# cli/options/pack_builder.py

"""
SampleMindAI – Pack Builder
Build a sample pack from selected audio files, organizing them by attributes (e.g., genre, mood).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def build_sample_pack(source_folder: str, destination_folder: str) -> None:
    """
    Placeholder function for building a sample pack from selected audio files.
    In the future, this will organize files into a sample pack by metadata (e.g., genre, mood).
    """
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(source_folder) if f.endswith(tuple(config.SUPPORTED_EXTENSIONS))]
    if not files:
        console.print(f"[yellow]No audio files found in {source_folder}[/yellow]")
        return

    for file in files:
        file_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.copy(file_path, destination_path)
        console.print(f"[cyan]Added {file} to the sample pack[/cyan]")
        log_event(f"Added {file} to the sample pack at {destination_folder}")

def main() -> None:
    """
    CLI entrypoint for building a sample pack.
    """
    console.print("[bold magenta]SampleMindAI – Pack Builder[/bold magenta]")

    source_folder = Prompt.ask("Enter the source folder", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_folder):
        console.print(f"[red]Source folder '{source_folder}' does not exist. Aborting.[/red]")
        return

    destination_folder = Prompt.ask("Enter the destination folder for the sample pack", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/red]")
        return

    build_sample_pack(source_folder, destination_folder)

    console.print(f"[green]Sample pack created successfully in {destination_folder}[/green]")
    log_event(f"Sample pack created from {source_folder} to {destination_folder}")

if __name__ == "__main__":
    main()
