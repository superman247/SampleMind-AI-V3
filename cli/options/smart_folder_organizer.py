# cli/options/smart_folder_organizer.py

"""
SampleMindAI – Smart Folder Organizer
Organize audio files into folders based on metadata tags (e.g., genre, mood, instrument).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil
import json

console = Console()

def organize_by_metadata(folder: str) -> None:
    """
    Placeholder function for organizing audio files into folders based on metadata.
    In the future, this will organize files based on tags like genre, mood, etc.
    """
    files = [f for f in os.listdir(folder) if f.endswith(tuple(config.SUPPORTED_EXTENSIONS))]
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return

    for file in files:
        file_path = os.path.join(folder, file)
        json_path = os.path.splitext(file_path)[0] + ".json"

        # Placeholder logic: create folders based on file extension
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                metadata = json.load(f)
                genre = metadata.get("genre", "Unknown Genre")
                genre_folder = os.path.join(folder, genre)

                if not os.path.exists(genre_folder):
                    os.makedirs(genre_folder)
                    console.print(f"[cyan]Created folder: {genre_folder}[/cyan]")

                # Move the file to the corresponding folder
                shutil.move(file_path, os.path.join(genre_folder, file))
                console.print(f"[cyan]Moved {file} to {genre_folder}[/cyan]")

                log_event(f"Moved {file} to {genre_folder}")

def main() -> None:
    """
    CLI entrypoint for organizing audio files by metadata.
    """
    console.print("[bold magenta]SampleMindAI – Smart Folder Organizer[/bold magenta]")

    folder = Prompt.ask("Enter the folder to organize", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    organize_by_metadata(folder)

    console.print(f"[green]Files organized by metadata![/green]")
    log_event(f"Files organized by metadata in {folder}")

if __name__ == "__main__":
    main()
