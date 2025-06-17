# cli/options/filter_by_tags.py

"""
SampleMindAI – Filter By Tags Module
Filter audio files in a folder/library by tags (genre, mood, instrument, etc).
Config-driven, Pylance-clean, with robust error handling.
"""

import os
import json
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def load_tags(json_path: str) -> Optional[Dict[str, str]]:
    """Loads tag data from .json file, returns None if not a dict or invalid."""
    try:
        with open(json_path, "r") as f:
            data: Any = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return None

def filter_files_by_tags(file_list: List[str], tag_filter: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Returns a list of dicts: {'path': ..., 'tags': {...}} for files matching the tag_filter.
    Skips files with invalid tag JSONs (str, list, etc).
    """
    matches = []
    for f in file_list:
        json_path = os.path.splitext(f)[0] + ".json"
        tags = load_tags(json_path)
        if not isinstance(tags, dict):
            continue
        if all(
            not v or (isinstance(tags.get(k, ""), str) and tags.get(k, "").lower() == v.lower())
            for k, v in tag_filter.items()
        ):
            matches.append({"path": f, "tags": tags})
    return matches

def display_results(results: List[Dict[str, Any]]) -> None:
    """Display filtered results in a Rich table."""
    table = Table(title="Filtered Samples")
    table.add_column("File")
    table.add_column("Genre")
    table.add_column("Mood")
    table.add_column("Instrument")

    for item in results:
        tags = item["tags"]
        table.add_row(
            os.path.basename(item["path"]),
            tags.get("genre", "") if isinstance(tags, dict) else "",
            tags.get("mood", "") if isinstance(tags, dict) else "",
            tags.get("instrument", "") if isinstance(tags, dict) else ""
        )
    console.print(table)

def main() -> None:
    """
    CLI entrypoint for filtering audio files by tags and displaying the results.
    """
    console.print("[bold magenta]SampleMindAI – Filter By Tags[/bold magenta]")
    folder = Prompt.ask("Scan folder", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    genre = Prompt.ask("Filter by genre (leave blank for any)", default="")
    mood = Prompt.ask("Filter by mood (leave blank for any)", default="")
    instrument = Prompt.ask("Filter by instrument (leave blank for any)", default="")
    tag_filter = {"genre": genre, "mood": mood, "instrument": instrument}

    all_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    filtered = filter_files_by_tags(all_files, tag_filter)

    if not filtered:
        console.print(f"[yellow]No files found matching the selected filters.[/]")
        return

    display_results(filtered)
    log_event(f"Filtered by tags: {tag_filter} ({len(filtered)} results)")

if __name__ == "__main__":
    main()
