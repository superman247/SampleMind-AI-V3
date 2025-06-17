# cli/options/smart_classifier.py

"""
SampleMindAI – Smart Classifier Module
Classifies a single audio file (or all in a folder) using Hermes AI (primary) and CNN (fallback).
Config-driven, robust, with Rich CLI, logging, and full error handling.
"""

import os
import json
from typing import Dict, Optional, List, Union
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def classify_file(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Classify a single audio file using the selected AI backend.
    Returns a dictionary of tags or None if classification fails.
    """
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        if tags and all(v and str(v).lower() not in {"", "unknown", "none"} for v in tags.values()):
            log_event(f"Classified: {audio_path} [{tags}]")
            return tags
        else:
            console.print(f"[yellow]AI returned invalid tags for {audio_path}[/]")
            log_event(f"AI invalid tags for {audio_path}: {tags}")
            return None
    except Exception as e:
        console.print(f"[red]Failed to classify {audio_path}: {e}[/]")
        log_event(f"Classification failed for {audio_path}: {e}")
        return None

def classify_and_save(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """
    Classifies the audio file and saves its tags to a .json file.
    """
    tags = classify_file(audio_path, ai_backend)
    if tags:
        json_path = os.path.splitext(audio_path)[0] + ".json"
        with open(json_path, "w") as f:
            json.dump(tags, f, indent=2)
        console.print(f"[green]Classified and saved: {audio_path} -> {json_path}[/]", highlight=False)
        return tags
    else:
        return None

def classify_folder(folder: str, ai_backend: str) -> List[Dict[str, str]]:
    """
    Batch classify all audio files in a folder.
    Returns a list of tag dictionaries.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not audio_files:
        console.print(f"[yellow]No audio files found in {folder}[/]")
        return []
    console.print(f"[bold cyan]Classifying {len(audio_files)} files in {folder}...[/]")
    results = []
    for audio_path in track(audio_files, description="Classifying"):
        tags = classify_and_save(audio_path, ai_backend)
        if tags:
            results.append({"path": audio_path, **tags})
    return results

def main() -> None:
    """
    CLI entrypoint for smart classification of audio files (single or batch).
    """
    console.print("[bold magenta]SampleMindAI – Smart Classifier[/bold magenta]")
    mode = Prompt.ask("Classify [1] single file or [2] all in folder?", choices=["1", "2"], default="1")

    ai_backend = config.AI_BACKEND

    if mode == "1":
        file_path = console.input(f"Enter path to audio file: ").strip()
        if not os.path.isfile(file_path):
            console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
            return
        classify_and_save(file_path, ai_backend)
    else:
        folder = console.input(f"Enter folder to scan for audio files [{config.SAMPLES_DIR}]: ").strip() or config.SAMPLES_DIR
        if not os.path.isdir(folder):
            console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
            return
        classify_folder(folder, ai_backend)

    console.print("[bold green]Smart classification process complete![/bold green]")

if __name__ == "__main__":
    main()
