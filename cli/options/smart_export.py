# cli/options/smart_export.py

"""
SampleMindAI – Smart Export
Export audio files and their metadata to a specified directory.
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

def export_classified_file(file_path: str, destination_folder: str) -> None:
    """
    Placeholder function for exporting classified audio files with metadata.
    This will copy the file and its metadata to a destination folder.
    """
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
        return

    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    # Copy audio file to the destination folder
    destination_file_path = os.path.join(destination_folder, os.path.basename(file_path))
    shutil.copy(file_path, destination_file_path)

    # Export associated metadata (if available)
    json_path = os.path.splitext(file_path)[0] + ".json"
    if os.path.exists(json_path):
        destination_json_path = os.path.splitext(destination_file_path)[0] + ".json"
        shutil.copy(json_path, destination_json_path)

    console.print(f"[cyan]Exported {file_path} and metadata to {destination_folder}[/cyan]")
    log_event(f"Exported {file_path} and metadata to {destination_folder}")

def main() -> None:
    """
    CLI entrypoint for exporting classified files and their metadata.
    """
    console.print("[bold magenta]SampleMindAI – Smart Export[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file to export")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/]")
        return

    destination_folder = Prompt.ask("Enter the destination folder", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Folder '{destination_folder}' does not exist. Aborting.[/]")
        return

    export_classified_file(file_path, destination_folder)

    console.print(f"[green]File export complete!{file_path} exported to {destination_folder}[/green]")
    log_event(f"File export complete for {file_path} to {destination_folder}")

if __name__ == "__main__":
    main()
