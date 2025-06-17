# cli/options/batch_reanalyze.py

"""
SampleMindAI – Batch Reanalyze Module
Batch reanalyzes all audio files in a folder and overwrites their tags with the current AI backend.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
from typing import List, Dict
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def reanalyze_and_tag(audio_path: str, ai_backend: str) -> Dict[str, str]:
    """
    Tags an audio file using the selected AI backend and overwrites its .json metadata.
    Returns the tag dict.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        json_path = os.path.splitext(audio_path)[0] + ".json"
        with open(json_path, "w") as f:
            json.dump(tags, f, indent=2)
        log_event(f"Batch reanalyze: {audio_path} -> {tags}")
        return tags
    except Exception as e:
        console.print(f"[red]Failed to reanalyze {audio_path}: {e}[/]")
        log_event(f"Reanalyze error for {audio_path}: {e}")
        return {}

def batch_reanalyze(folder: str, ai_backend: str) -> int:
    """
    Batch reanalyzes all supported audio files in the folder.
    Overwrites all .json tags.
    Returns the count of files processed.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not audio_files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return 0

    console.print(f"[bold cyan]Batch reanalyzing {len(audio_files)} audio files in {folder}...[/bold cyan]")
    processed = 0

    for audio_path in track(audio_files, description="Reanalyzing"):
        tags = reanalyze_and_tag(audio_path, ai_backend)
        if tags:
            processed += 1

    return processed

def main() -> None:
    """
    CLI entrypoint for batch reanalyzing all audio files and updating tags.
    """
    console.print("[bold magenta]SampleMindAI – Batch Reanalyze[/bold magenta]")
    folder = Prompt.ask("Folder to reanalyze", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    ai_backend = config.AI_BACKEND
    confirm = Confirm.ask("This will overwrite all .json tags in this folder. Proceed?", default=False)
    if not confirm:
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    count = batch_reanalyze(folder, ai_backend)
    if count > 0:
        console.print(f"[green]Reanalyzed and updated {count} files.[/green]")
    else:
        console.print("[yellow]No files reanalyzed.[/yellow]")

if __name__ == "__main__":
    main()
