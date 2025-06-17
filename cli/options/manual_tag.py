# cli/options/manual_tag.py

"""
SampleMindAI – Manual Tag Module
Manually tag audio files with genre, mood, instrument, and save metadata as .json.
Batch or single file mode. Config-driven, Pylance-clean, and robust.
"""

import os
import json
from typing import List, Dict, Any
from rich.console import Console
from rich.prompt import Prompt

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def manual_tag_file(audio_path: str) -> Dict[str, str]:
    """Prompt the user for tags and return a dict."""
    console.print(f"\n[bold]Tagging: {os.path.basename(audio_path)}[/bold]")
    genre = Prompt.ask("Genre", default="")
    mood = Prompt.ask("Mood", default="")
    instrument = Prompt.ask("Instrument", default="")
    tags = {"genre": genre, "mood": mood, "instrument": instrument}
    return tags

def save_tags(audio_path: str, tags: Dict[str, str]) -> None:
    """Save tags to a .json file beside the audio file."""
    json_path = os.path.splitext(audio_path)[0] + ".json"
    with open(json_path, "w") as f:
        json.dump(tags, f, indent=2)
    log_event(f"Manual tags saved: {audio_path} [{tags}]")
    console.print(f"[green]Saved tags for {os.path.basename(audio_path)}[/green]")

def main() -> None:
    """
    CLI entrypoint for manual tagging.
    User can choose to tag a single file or all files in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Manual Tag[/bold magenta]")
    mode = Prompt.ask("Tag [1] single file or [2] all in folder?", choices=["1", "2"], default="1")

    if mode == "1":
        file_path = Prompt.ask("Enter path to audio file")
        if not os.path.isfile(file_path):
            console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
            return
        tags = manual_tag_file(file_path)
        save_tags(file_path, tags)
    else:
        folder = Prompt.ask("Folder to tag", default=config.SAMPLES_DIR)
        if not os.path.isdir(folder):
            console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
            return
        files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
        if not files:
            console.print(f"[yellow]No audio files found in {folder}[/]")
            return
        for f in files:
            tags = manual_tag_file(f)
            save_tags(f, tags)

    console.print("[bold green]Manual tagging process complete![/bold green]")

if __name__ == "__main__":
    main()
