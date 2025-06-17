# cli/options/ai_reanalyze.py

"""
SampleMindAI – AI Reanalyze Tool
Batch reanalyze and overwrite all tags for audio files in a folder using the current AI backend (Hermes/CNN).
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
from typing import Dict, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def reanalyze_file(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Retag an audio file using the current AI backend and overwrite its .json metadata.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        json_path = os.path.splitext(audio_path)[0] + ".json"
        with open(json_path, "w") as f:
            json.dump(tags, f, indent=2)
        console.print(f"[green]Reanalyzed: {audio_path} -> {tags}[/green]")
        log_event(f"AI reanalyze: {audio_path} [{tags}]")
        return tags
    except Exception as e:
        console.print(f"[red]Failed to reanalyze {audio_path}: {e}[/red]")
        log_event(f"AI reanalyze failed: {audio_path}: {e}")
        return None

def main() -> None:
    """
    CLI entrypoint for batch reanalyzing audio files and updating their tags.
    """
    console.print("[bold magenta]SampleMindAI – AI Reanalyze Tool[/bold magenta]")
    folder = Prompt.ask("Folder to reanalyze", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    confirm = Confirm.ask("This will overwrite all .json tags in this folder. Proceed?", default=False)
    if not confirm:
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    ai_backend = config.AI_BACKEND
    files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return

    for f in track(files, description="Reanalyzing"):
        reanalyze_file(f, ai_backend)

    console.print("[bold green]AI reanalyze complete![/bold green]")

if __name__ == "__main__":
    main()
