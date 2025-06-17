# cli/options/auto_json_tag.py

"""
SampleMindAI – Auto JSON Tag Module
Automatically generates or updates .json metadata for audio files using Hermes AI (primary)
and fallback methods. Robust, batch-supporting, config-driven, and Pylance-clean.
"""

import os
import json
from typing import Dict, Optional
from rich.console import Console
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def is_tag_valid(tag_dict: Dict[str, str]) -> bool:
    """
    Checks if the tag dictionary has non-empty, non-'unknown' values for required fields.
    """
    for v in tag_dict.values():
        if not v or str(v).lower() in {"", "unknown", "none"}:
            return False
    return True

def tag_and_write_json(audio_path: str, json_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Runs AI tagging and writes valid tags to the json file.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        if is_tag_valid(tags):
            with open(json_path, "w") as f:
                json.dump(tags, f, indent=2)
            log_event(f"Tagged {audio_path} -> {json_path} [{tags}]")
            return tags
        else:
            console.print(f"[yellow]AI returned invalid tags for {audio_path}. Skipped.[/]")
            log_event(f"AI invalid tags for {audio_path}: {tags}")
            return None
    except Exception as e:
        console.print(f"[red]Failed to tag {audio_path}: {e}[/]")
        log_event(f"Tagging failed for {audio_path}: {e}")
        return None

def auto_tag_json_in_folder(folder: str, ai_backend: str) -> None:
    """
    Batch process: For every audio file, ensure .json exists with valid tags.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not audio_files:
        console.print(f"[yellow]No audio files found in {folder}[/]")
        return

    console.print(f"[bold cyan]Processing {len(audio_files)} files in {folder}...[/]")

    for audio_path in track(audio_files, description="Tagging audio"):
        json_path = os.path.splitext(audio_path)[0] + ".json"
        write_needed = True

        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    existing = json.load(f)
                if is_tag_valid(existing):
                    write_needed = False
                    console.print(f"[green]Valid JSON exists for {audio_path}[/]", highlight=False)
            except Exception:
                write_needed = True

        if write_needed:
            tag_and_write_json(audio_path, json_path, ai_backend)

def main() -> None:
    """
    CLI entrypoint for batch auto-tagging all audio files in a folder (creates .json files).
    """
    console.print("[bold magenta]SampleMindAI – Auto JSON Tag[/bold magenta]")
    folder = console.input(f"Enter folder to scan for audio files [{config.SAMPLES_DIR}]: ").strip() or config.SAMPLES_DIR
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    ai_backend = config.AI_BACKEND
    auto_tag_json_in_folder(folder, ai_backend)

    console.print("[bold green]Auto JSON tag process complete![/bold green]")

if __name__ == "__main__":
    main()
