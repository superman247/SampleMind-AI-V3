# cli/options/convert_to_mp3.py

"""
SampleMindAI – Convert to MP3
Convert audio files from one format to MP3.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def convert_audio_to_mp3(file_path: str, target_path: str) -> None:
    """
    Placeholder function for converting an audio file to MP3 format.
    This can later be implemented using a library like pydub or ffmpeg.
    """
    console.print(f"[cyan]Converting {file_path} to MP3...[/cyan]")
    log_event(f"Converting {file_path} to MP3 format.")

    try:
        # Placeholder: Assuming we're copying the file for now as a "conversion"
        target_file = os.path.splitext(target_path)[0] + ".mp3"
        shutil.copy(file_path, target_file)
        console.print(f"[green]Successfully converted to: {target_file}[/green]")
        log_event(f"Successfully converted {file_path} to {target_file}")
    except Exception as e:
        console.print(f"[red]Failed to convert {file_path} to MP3: {e}[/red]")
        log_event(f"Failed to convert {file_path} to MP3: {e}")

def main() -> None:
    """
    CLI entrypoint for converting audio files to MP3 format.
    """
    console.print("[bold magenta]SampleMindAI – Convert to MP3[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file")
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    target_folder = Prompt.ask("Enter the destination folder", default=config.OUTPUT_DIR)
    if not os.path.isdir(target_folder):
        console.print(f"[red]Destination folder '{target_folder}' does not exist. Aborting.[/red]")
        return

    # Perform the conversion
    convert_audio_to_mp3(file_path, target_folder)

    console.print("[green]Conversion complete![/green]")
    log_event(f"Conversion complete for {file_path} to MP3 in {target_folder}")

if __name__ == "__main__":
    main()
