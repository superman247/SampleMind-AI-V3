# cli/options/build_pack.py

"""
SampleMindAI – Build Sample Pack
Create and organize a sample pack from selected audio files.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def create_sample_pack(source_folder: str, destination_folder: str) -> None:
    """
    Placeholder for creating a sample pack from selected audio files.
    The idea is to collect, organize, and copy the files into a pack.
    """
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(source_folder) if f.endswith(".wav")]
    if not files:
        console.print(f"[yellow]No .wav files found in {source_folder}[/yellow]")
        return

    for file in files:
        src_path = os.path.join(source_folder, file)
        dst_path = os.path.join(destination_folder, file)
        shutil.copy(src_path, dst_path)
        console.print(f"[cyan]Added {file} to sample pack[/cyan]")
        log_event(f"Sample pack creation: {file} added from {source_folder} to {destination_folder}")

def main() -> None:
    """
    CLI entrypoint for building a sample pack.
    Placeholder for sample pack creation functionality.
    """
    console.print("[bold magenta]SampleMindAI – Build Sample Pack[/bold magenta]")

    source_folder = Prompt.ask("Enter the folder with samples", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_folder):
        console.print(f"[red]Folder '{source_folder}' does not exist. Aborting.[/red]")
        return

    destination_folder = Prompt.ask("Enter the destination folder for the sample pack", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/red]")
        return

    create_sample_pack(source_folder, destination_folder)
    console.print(f"[green]Sample pack created in {destination_folder}[/green]")
    log_event(f"Sample pack created from {source_folder} to {destination_folder}")

if __name__ == "__main__":
    main()
