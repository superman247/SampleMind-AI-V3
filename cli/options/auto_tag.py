# cli/options/auto_tag.py

"""
SampleMindAI – Auto Tag Module
Automatically tags all audio files in a folder using Hermes AI (primary) or fallback.
Supports batch mode, config-driven paths, robust error handling, and Pylance-clean code.
"""

import os
from typing import Dict, Optional
from rich.console import Console
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

import json

console = Console()

def is_tag_valid(tags: Dict[str, str]) -> bool:
    """
    Checks if the tag dictionary has valid (non-empty, non-'unknown') values.
    """
    for v in tags.values():
        if not v or str(v).lower() in {"", "unknown", "none"}:
            return False
    return True

def auto_tag_file(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Run AI tagging and return tags. Log and print errors as needed.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        if is_tag_valid(tags):
            log_event(f"Tagged: {audio_path} [{tags}]")
            return tags
        else:
            console.print(f"[yellow]AI returned invalid tags for {audio_path}[/]")
            log_event(f"AI invalid tags for {audio_path}: {tags}")
            return None
    except Exception as e:
        console.print(f"[red]Failed to tag {audio_path}: {e}[/]")
        log_event(f"Tagging failed for {audio_path}: {e}")
        return None

def auto_tag_folder(folder: str, ai_backend: str) -> None:
    """
    Batch-tag all audio files in the given folder and print/save their tags.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not audio_files:
        console.print(f"[yellow]No audio files found in {folder}[/]")
        return

    console.print(f"[bold cyan]Tagging {len(audio_files)} audio files in {folder}...[/]")

    for audio_path in track(audio_files, description="Auto-tagging"):
        tags = auto_tag_file(audio_path, ai_backend)
        if tags:
            json_path = os.path.splitext(audio_path)[0] + ".json"
            with open(json_path, "w") as f:
                json.dump(tags, f, indent=2)
            console.print(f"[green]Tagged and saved: {audio_path}[/]", highlight=False)

def main() -> None:
    """
    CLI entrypoint for auto-tagging all audio files in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Auto Tag[/bold magenta]")
    folder = console.input(f"Enter folder to scan for audio files [{config.SAMPLES_DIR}]: ").strip() or config.SAMPLES_DIR
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    ai_backend = config.AI_BACKEND
    auto_tag_folder(folder, ai_backend)

    console.print("[bold green]Auto-tagging process complete![/bold green]")

if __name__ == "__main__":
    main()
