# cli/options/map_favorites.py

"""
SampleMindAI – Map Favorites
Map favorite audio files for easy access and future operations (e.g., export, processing).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def map_favorite_audio(file_path: str) -> None:
    """
    Placeholder function to add a file to the favorites map.
    In the future, this will store and allow for operations on favorite files.
    """
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return
    
    favorites_file = os.path.join(config.OUTPUT_DIR, "favorites.json")

    # Placeholder logic: Add file to favorites list (this could be expanded to include more metadata)
    favorite_data = []
    if os.path.exists(favorites_file):
        with open(favorites_file, "r") as f:
            favorite_data = json.load(f)
    
    favorite_data.append(file_path)

    with open(favorites_file, "w") as f:
        json.dump(favorite_data, f, indent=2)

    console.print(f"[cyan]Mapped {file_path} as a favorite[/cyan]")
    log_event(f"Mapped {file_path} as a favorite")

def main() -> None:
    """
    CLI entrypoint for mapping favorite audio files.
    """
    console.print("[bold magenta]SampleMindAI – Map Favorites[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file to mark as a favorite")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    map_favorite_audio(file_path)

    console.print(f"[green]Mapping complete! {file_path} added to favorites.[/green]")
    log_event(f"Mapping complete for {file_path} to favorites")

if __name__ == "__main__":
    main()
