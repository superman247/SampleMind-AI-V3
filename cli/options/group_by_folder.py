# cli/options/group_by_folder.py

"""
SampleMindAI – Group By Folder
Group audio files into folders based on a specific attribute or metadata.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def group_files_by_folder(source_folder: str, destination_folder: str) -> None:
    """
    Placeholder function for grouping audio files into folders based on metadata.
    Currently just simulates the grouping of files based on their extension.
    """
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(source_folder) if f.endswith(tuple(config.SUPPORTED_EXTENSIONS))]
    if not files:
        console.print(f"[yellow]No audio files found in {source_folder}[/yellow]")
        return

    # Placeholder: Group files by their extension for now
    for file in files:
        file_extension = file.split(".")[-1]
        target_folder = os.path.join(destination_folder, file_extension)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        src_path = os.path.join(source_folder, file)
        dst_path = os.path.join(target_folder, file)
        shutil.move(src_path, dst_path)
        console.print(f"[cyan]Moved {file} to {target_folder}[/cyan]")
        log_event(f"Grouped {file} into {target_folder}")

def main() -> None:
    """
    CLI entrypoint for grouping audio files by folder.
    """
    console.print("[bold magenta]SampleMindAI – Group By Folder[/bold magenta]")

    source_folder = Prompt.ask("Enter the source folder", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_folder):
        console.print(f"[red]Source folder '{source_folder}' does not exist. Aborting.[/red]")
        return

    destination_folder = Prompt.ask("Enter the destination folder", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/red]")
        return

    group_files_by_folder(source_folder, destination_folder)

    console.print(f"[green]Files grouped successfully in {destination_folder}[/green]")
    log_event(f"Files grouped from {source_folder} to {destination_folder}")

if __name__ == "__main__":
    main()
