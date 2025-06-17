# cli/options/ai_analysis.py

"""
SampleMindAI – AI Analysis Tool
Analyze one or many audio files using the current AI backend (Hermes/CNN), printing and saving tags.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
from typing import Dict, Optional, List
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def ai_analyze_file(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Tag an audio file using the selected AI backend and print/save the results.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        json_path = os.path.splitext(audio_path)[0] + ".json"
        with open(json_path, "w") as f:
            json.dump(tags, f, indent=2)
        console.print(f"[green]Analyzed: {audio_path} -> {tags}[/green]")
        log_event(f"AI analysis: {audio_path} [{tags}]")
        return tags
    except Exception as e:
        console.print(f"[red]Failed to analyze {audio_path}: {e}[/red]")
        log_event(f"AI analysis failed: {audio_path}: {e}")
        return None

def main() -> None:
    """
    CLI entrypoint for AI-powered audio file analysis (single or batch).
    """
    console.print("[bold magenta]SampleMindAI – AI Analysis Tool[/bold magenta]")
    mode = Prompt.ask("Analyze [1] single file or [2] all in folder?", choices=["1", "2"], default="1")

    ai_backend = config.AI_BACKEND

    if mode == "1":
        file_path = Prompt.ask("Path to audio file")
        if not os.path.isfile(file_path):
            console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
            return
        ai_analyze_file(file_path, ai_backend)
    else:
        folder = Prompt.ask("Folder to analyze", default=config.SAMPLES_DIR)
        if not os.path.isdir(folder):
            console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
            return
        files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
        if not files:
            console.print(f"[yellow]No audio files found in {folder}[/yellow]")
            return
        for f in track(files, description="Analyzing"):
            ai_analyze_file(f, ai_backend)

    console.print("[bold green]AI analysis complete![/bold green]")

if __name__ == "__main__":
    main()
