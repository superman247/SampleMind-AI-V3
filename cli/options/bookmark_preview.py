# cli/options/bookmark_preview.py

"""
SampleMindAI – Bookmark Preview Module
Preview and play all bookmarked samples/loops as a playlist. Optionally unbookmark files on the fly.
Pylance-clean, config-driven, cross-platform, with Rich CLI and robust error handling.
"""

import os
import json
import platform
import subprocess
from typing import List
from rich.console import Console
from rich.prompt import Prompt

from utils.config import config
from utils.logger import log_event

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
            startfile = getattr(os, "startfile", None)
            if callable(startfile):
                startfile(filepath)  # type: ignore
            else:
                subprocess.run(["start", filepath], shell=True, check=False)
        else:  # Linux/other
            if filepath.lower().endswith(".wav"):
                subprocess.run(["aplay", filepath], check=False)
            else:
                subprocess.run(["xdg-open", filepath], check=False)
    except Exception as e:
        console.print(f"[red]Failed to play audio: {e}[/]")

def main() -> None:
    """
    CLI entrypoint for previewing all bookmarked samples/loops as a playlist.
    """
    console.print("[bold magenta]SampleMindAI – Bookmark Preview[/bold magenta]")

    bookmarks = load_bookmarks()
    if not bookmarks:
        console.print("[yellow]No bookmarks found. Use the Bookmark Explorer first.[/yellow]")
        return

    while True:
        console.print("\n[bold]Bookmarked Samples:[/bold]")
        for idx, f in enumerate(bookmarks):
            console.print(f"{idx + 1}. {os.path.basename(f)}")

        console.print("\nOptions: [b][P][/b]review, [b][U][/b]nbookmark, [b][Q][/b]uit")
        cmd = Prompt.ask("Enter option").strip().lower()

        if cmd == "q":
            break
        elif cmd == "p":
            num = Prompt.ask("Enter file number to play (or 'all' for playlist)", default="1")
            if num == "all":
                for f in bookmarks:
                    preview_audio(f)
            else:
                try:
                    idx = int(num) - 1
                    if idx < 0 or idx >= len(bookmarks):
                        raise ValueError
                    preview_audio(bookmarks[idx])
                except Exception:
                    console.print("[red]Invalid selection.[/red]")
        elif cmd == "u":
            num = Prompt.ask("Enter file number to unbookmark", default="1")
            try:
                idx = int(num) - 1
                if idx < 0 or idx >= len(bookmarks):
                    raise ValueError
                removed = bookmarks.pop(idx)
                save_bookmarks(bookmarks)
                console.print(f"[green]Removed bookmark for {os.path.basename(removed)}[/green]")
            except Exception:
                console.print("[red]Invalid selection.[/red]")
        else:
            console.print("[yellow]Unknown command.[/yellow]")

    console.print("[bold green]Bookmark Preview exited.[/bold green]")

if __name__ == "__main__":
    main()
