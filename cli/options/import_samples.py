# cli/options/import_samples.py

"""
SampleMindAI – Import Samples
Import audio samples into the library and automatically assign metadata tags.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def import_sample(file_path: str, destination_folder: str) -> None:
    """
    Placeholder function for importing a sample and assigning metadata tags.
    In the future, this would assign tags based on AI classification or metadata extraction.
    """
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)
    
    shutil.copy(file_path, destination_path)
    console.print(f"[cyan]Imported {file_name} to {destination_folder}[/cyan]")

    # Placeholder: Here we would assign metadata tags (e.g., genre, mood, instrument) to the sample
    log_event(f"Imported sample: {file_name} to {destination_folder}")

def main() -> None:
    """
    CLI entrypoint for importing samples into the system.
    """
    console.print("[bold magenta]SampleMindAI – Import Samples[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio sample")
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    destination_folder = Prompt.ask("Enter the destination folder for the sample", default=config.SAMPLES_DIR)
    if not os.path.isdir(destination_folder):
        console.print(f"[red]Destination folder '{destination_folder}' does not exist. Aborting.[/red]")
        return

    import_sample(file_path, destination_folder)

    console.print(f"[green]Sample import complete![/green]")
    log_event(f"Sample import complete for {file_path} to {destination_folder}")

if __name__ == "__main__":
    main()
