# cli/options/bookmark_explorer.py

"""
SampleMindAI – Bookmark Explorer Module
Browse, preview, and bookmark audio files interactively in your sample/loop library.
Pylance-clean, config-driven, with Rich CLI and robust error handling.
"""

import os
import json
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files
import subprocess
import platform

BOOKMARKS_FILE = os.path.join(config.OUTPUT_DIR, "bookmarked_samples.json")
console = Console()

def load_bookmarks() -> List[str]:
    """Load the list of bookmarked file paths."""
    if not os.path.isfile(BOOKMARKS_FILE):
        return []
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

def save_bookmarks(bookmarks: List[str]) -> None:
    """Save the list of bookmarked file paths."""
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f, indent=2)
    log_event(f"Bookmarked files updated: {len(bookmarks)} items")

def preview_audio(filepath: str) -> None:
    """Plays a short preview of the audio file using system player (cross-platform)."""
    console.print(f"[cyan]Previewing: {filepath}[/cyan]")
    try:
        sys_platform = platform.system()
        if sys_platform == "Darwin":  # macOS
            subprocess.run(["afplay", filepath], check=False)
        elif sys_platform == "Windows":
            # Only use startfile if it exists (and ignore for type checking)
            startfile = getattr(os, "startfile", None)
            if callable(startfile):
                startfile(filepath)  # type: ignore
            else:
                subprocess.run(["start", filepath], shell=True, check=False)
        else:  # Linux/other
            # Try aplay for WAVs, or xdg-open for general
            if filepath.lower().endswith(".wav"):
                subprocess.run(["aplay", filepath], check=False)
            else:
                subprocess.run(["xdg-open", filepath], check=False)
    except Exception as e:
        console.print(f"[red]Failed to play audio: {e}[/]")



def show_table(files: List[str], bookmarks: List[str]) -> None:
    """Displays a Rich table of files, showing bookmarked ones with a mark."""
    table = Table(title="Sample/Loop Library")
    table.add_column("No.", style="cyan", width=5)
    table.add_column("File", style="white")
    table.add_column("Bookmarked", style="green", width=10)

    for idx, f in enumerate(files):
        is_bookmarked = "★" if f in bookmarks else ""
        table.add_row(str(idx + 1), os.path.basename(f), is_bookmarked)
    console.print(table)

def main() -> None:
    """
    CLI entry for exploring and bookmarking samples/loops interactively.
    """
    console.print("[bold magenta]SampleMindAI – Bookmark Explorer[/bold magenta]")
    folder = Prompt.ask("Library folder", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/]")
        return

    bookmarks = load_bookmarks()

    while True:
        show_table(files, bookmarks)
        console.print("[bold]Options:[/bold] [b][P][/b]review | [b][B][/b]ookmark | [b][U][/b]nbookmark | [b][L][/b]ist bookmarks | [b][Q][/b]uit")
        cmd = Prompt.ask("Enter option").strip().lower()

        if cmd == "q":
            break
        elif cmd == "l":
            if not bookmarks:
                console.print("[yellow]No bookmarks yet.[/yellow]")
            else:
                for idx, path in enumerate(bookmarks, 1):
                    console.print(f"{idx}. {os.path.basename(path)}")
        elif cmd in {"p", "b", "u"}:
            num = Prompt.ask("Enter file number", default="1")
            try:
                idx = int(num) - 1
                if idx < 0 or idx >= len(files):
                    raise ValueError
                selected_file = files[idx]
            except Exception:
                console.print("[red]Invalid selection.[/red]")
                continue
            if cmd == "p":
                preview_audio(selected_file)
            elif cmd == "b":
                if selected_file not in bookmarks:
                    bookmarks.append(selected_file)
                    save_bookmarks(bookmarks)
                    console.print(f"[green]Bookmarked {os.path.basename(selected_file)}[/green]")
                else:
                    console.print("[yellow]Already bookmarked.[/yellow]")
            elif cmd == "u":
                if selected_file in bookmarks:
                    bookmarks.remove(selected_file)
                    save_bookmarks(bookmarks)
                    console.print(f"[green]Removed bookmark for {os.path.basename(selected_file)}[/green]")
                else:
                    console.print("[yellow]File not bookmarked.[/yellow]")
        else:
            console.print("[yellow]Unknown command.[/yellow]")

    console.print("[bold green]Bookmark Explorer exited.[/bold green]")

if __name__ == "__main__":
    main()
