# cli/options/sort_by_attribute.py

"""
SampleMindAI – Sort By Attribute
Sort audio files into folders based on metadata tags (e.g., genre, mood, instrument).
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

def sort_audio_files_by_attribute(folder: str, attribute: str) -> None:
    """
    Placeholder function for sorting audio files based on metadata attributes.
    In the future, this will sort files by tags like genre, mood, etc.
    """
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
                attribute_value = metadata.get(attribute, "Unknown")

                # Create a folder for the attribute value if it doesn't exist
                attribute_folder = os.path.join(folder, attribute_value)
                if not os.path.exists(attribute_folder):
                    os.makedirs(attribute_folder)
                    console.print(f"[cyan]Created folder: {attribute_folder}[/cyan]")

                # Move the file to the corresponding folder
                shutil.move(file_path, os.path.join(attribute_folder, file))
                console.print(f"[cyan]Moved {file} to {attribute_folder}[/cyan]")

                log_event(f"Sorted {file} into {attribute_folder}")

def main() -> None:
    """
    CLI entrypoint for sorting audio files by metadata attributes.
    """
    console.print("[bold magenta]SampleMindAI – Sort By Attribute[/bold magenta]")

    folder = Prompt.ask("Enter the folder to sort", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    attribute = Prompt.ask("Enter the metadata attribute to sort by (e.g., genre, mood)", default="genre")

    sort_audio_files_by_attribute(folder, attribute)

    console.print(f"[green]Files sorted by {attribute} attribute![/green]")
    log_event(f"Files sorted by {attribute} attribute in {folder}")

if __name__ == "__main__":
    main()
