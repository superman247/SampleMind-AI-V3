# cli/options/export_csv.py

"""
SampleMindAI – Export CSV
Export metadata of audio files to CSV format.
Future functionality; currently includes a placeholder.
"""

import os
import csv
from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files

console = Console()

def export_metadata_to_csv(folder: str, output_file: str) -> None:
    """
    Placeholder function for exporting audio metadata to a CSV file.
    """
    files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not files:
        console.print(f"[yellow]No audio files found in {folder}[/yellow]")
        return
    
    # Placeholder: Extract metadata from each file (using mock data for now)
    with open(output_file, "w", newline='') as csvfile:
        fieldnames = ['file_name', 'genre', 'mood', 'instrument']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file in files:
            # Mock metadata
            metadata = {
                'file_name': file,
                'genre': "Unknown Genre", 
                'mood': "Neutral Mood",
                'instrument': "Undefined Instrument"
            }
            writer.writerow(metadata)
            console.print(f"[cyan]Exporting: {file}[/cyan]")
            log_event(f"Exported {file} metadata to CSV")

    console.print(f"[green]Metadata exported to {output_file}[/green]")
    log_event(f"Metadata export complete for folder: {folder}")

def main() -> None:
    """
    CLI entrypoint for exporting metadata to CSV.
    """
    console.print("[bold magenta]SampleMindAI – Export CSV[/bold magenta]")

    folder = Prompt.ask("Enter the folder to export metadata from", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return
    
    output_file = Prompt.ask("Enter the path for the output CSV file", default=os.path.join(config.OUTPUT_DIR, "audio_metadata.csv"))
    
    export_metadata_to_csv(folder, output_file)

    console.print(f"[green]CSV export complete! Metadata saved to {output_file}[/green]")
    log_event(f"CSV export complete for folder: {folder} to {output_file}")

if __name__ == "__main__":
    main()
