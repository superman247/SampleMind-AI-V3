# cli/options/export_pack.py

"""
SampleMindAI – Export Pack Module
Exports a curated pack of samples/loops from your library with filtering by tags and smart selection.
Config-driven, robust, Pylance-clean, with Rich CLI and logging.
"""

import os
import shutil
import json
from typing import List, Dict, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def load_tags(json_path: str) -> Optional[Dict[str, str]]:
    """Loads tags from a .json file, returns None if missing or invalid."""
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return None
    except Exception:
        return None

def filter_files_by_tags(file_list: List[str], tag_filter: Dict[str, str]) -> List[str]:
    """
    Filters audio files by tags in their adjacent .json metadata.
    Only files whose tags match all keys/values in tag_filter are included.
    """
    filtered = []
    for f in file_list:
        json_path = os.path.splitext(f)[0] + ".json"
        tags = load_tags(json_path)
        if tags and all(tags.get(k, "").lower() == v.lower() for k, v in tag_filter.items() if v):
            filtered.append(f)
    return filtered

def export_files(files: List[str], export_dir: str) -> None:
    """Copies files and their .json metadata to the export directory."""
    ensure_folder_exists(export_dir)
    for f in track(files, description="Exporting"):
        try:
            shutil.copy2(f, export_dir)
            json_path = os.path.splitext(f)[0] + ".json"
            if os.path.exists(json_path):
                shutil.copy2(json_path, export_dir)
            log_event(f"Exported: {f}")
        except Exception as e:
            console.print(f"[red]Failed to export {f}: {e}[/]")
            log_event(f"Export failed for {f}: {e}")

def main() -> None:
    """
    CLI entrypoint for exporting a curated pack of audio files, filtered by tags.
    """
    console.print("[bold magenta]SampleMindAI – Export Pack[/bold magenta]")
    source_dir = Prompt.ask("Select source folder to export from", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_dir):
        console.print(f"[red]Folder '{source_dir}' does not exist. Aborting.[/]")
        return

    export_dir = Prompt.ask("Select export folder", default=os.path.join(config.OUTPUT_DIR, "exported_pack"))
    ensure_folder_exists(export_dir)

    # Prompt for simple tag filter (genre, mood, instrument)
    genre = Prompt.ask("Filter by genre (leave blank for any)", default="")
    mood = Prompt.ask("Filter by mood (leave blank for any)", default="")
    instrument = Prompt.ask("Filter by instrument (leave blank for any)", default="")
    tag_filter = {"genre": genre, "mood": mood, "instrument": instrument}

    all_files = find_all_audio_files(source_dir, config.SUPPORTED_EXTENSIONS)
    filtered_files = filter_files_by_tags(all_files, tag_filter) if any(tag_filter.values()) else all_files

    if not filtered_files:
        console.print(f"[yellow]No files found matching the selected filters.[/]")
        return

    console.print(f"[cyan]Exporting {len(filtered_files)} files to {export_dir}...[/cyan]")
    export_files(filtered_files, export_dir)

    console.print(f"[bold green]Export complete! {len(filtered_files)} files saved to {export_dir}[/bold green]")

if __name__ == "__main__":
    main()
