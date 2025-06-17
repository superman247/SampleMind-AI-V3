# cli/options/smart_pack_builder.py

"""
SampleMindAI – Smart Pack Builder
Build a sample pack from selected audio files, organized by metadata tags (e.g., genre, mood, instrument).
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

def build_sample_pack_from_metadata(folder: str, destination_folder: str) -> None:
    """
    Placeholder function to build a sample pack from selected audio files.
    In the future, this can organize the files based on metadata (e.g., genre, mood).
    """
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(folder) if f.endswith(tuple(config.SUPPORTED_EXTENSIONS))]
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return

    for file in files:
        file_path = os.path.join(folder, file)
        json_path = os.path.splitext(file_path)[0] + ".json"

        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                metadata = json.load(f)
                genre = metadata.get("genre", "Unknown Genre")
                genre_folder = os.path.join(destination_folder, genre)

                if not os.path.exists(genre_folder):
                    os.makedirs(genre_folder)
                    console.print(f"[cyan]Created folder: {genre_folder}[/cyan]")

                shutil.copy(file_path, os.path.join(genre_folder, file))
                console.print(f"[cyan]Added {file} to {genre_folder}[/cyan]")

                log_event(f"Added {file} to sample pack at {genre_folder}")

def main() -> None:
    """
    CLI entrypoint for building a sample pack.
    """
    console.print("[bold magenta]SampleMindAI – Smart Pack Builder[/bold magenta]")

    folder = Prompt.ask("Enter the folder with the audio files", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    destination_folder = Prompt.ask("Enter the destination folder for the sample pack", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/]")
        return

    build_sample_pack_from_metadata(folder, destination_folder)

    console.print(f"[green]Sample pack created successfully in {destination_folder}[/green]")
    log_event(f"Sample pack created from {folder} to {destination_folder}")

if __name__ == "__main__":
    main()
