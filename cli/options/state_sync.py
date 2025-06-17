# cli/options/state_sync.py

"""
SampleMindAI – State Sync
Sync the state of the project (e.g., settings, preferences) between different devices or sessions.
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

def sync_project_state(source_folder: str, destination_folder: str) -> None:
    """
    Placeholder function for syncing project state (e.g., settings, files, metadata).
    In the future, this could synchronize configurations, session data, or other parts of the project.
    """
    if not os.path.isdir(source_folder):
        console.print(f"[red]Source folder '{source_folder}' does not exist. Aborting.[/]")
        return
    
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)

    # Simulate syncing by copying all files from source to destination
    for file in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file)
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination_folder, file)
            shutil.copy(source_file, destination_file)
            console.print(f"[cyan]Synced: {file} from {source_folder} to {destination_folder}[/cyan]")
            log_event(f"Synced {file} from {source_folder} to {destination_folder}")

def main() -> None:
    """
    CLI entrypoint for syncing project state.
    """
    console.print("[bold magenta]SampleMindAI – State Sync[/bold magenta]")

    source_folder = Prompt.ask("Enter the source folder to sync", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_folder):
        console.print(f"[red]Source folder '{source_folder}' does not exist. Aborting.[/]")
        return

    destination_folder = Prompt.ask("Enter the destination folder to sync", default=config.OUTPUT_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/]")
        return

    sync_project_state(source_folder, destination_folder)

    console.print(f"[green]Project state synced successfully![/green]")
    log_event(f"Project state synced from {source_folder} to {destination_folder}")

if __name__ == "__main__":
    main()
