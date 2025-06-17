# cli/options/sample_splitter.py

"""
SampleMindAI – Sample Splitter
Split audio files into smaller segments (e.g., based on time, beats, etc.).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import shutil

console = Console()

def split_audio(file_path: str, segment_length: int) -> None:
    """
    Placeholder function for splitting an audio file into smaller segments.
    In the future, this could split the file by time or beats.
    """
    console.print(f"[cyan]Splitting audio file: {file_path} into {segment_length}-second segments[/cyan]")
    log_event(f"Splitting audio: {file_path} into {segment_length}-second segments")
    
    # Placeholder: Simulate splitting by copying the file to new paths
    base_name = os.path.splitext(file_path)[0]
    for i in range(3):  # Simulate 3 segments for now
        segment_file = f"{base_name}_segment_{i + 1}.wav"
        shutil.copy(file_path, segment_file)
        console.print(f"[cyan]Created segment: {segment_file}[/cyan]")
        log_event(f"Created segment: {segment_file}")

def main() -> None:
    """
    CLI entrypoint for splitting audio files.
    """
    console.print("[bold magenta]SampleMindAI – Sample Splitter[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file to split")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    # Remove type=int, and cast the input to int explicitly
    segment_length_input = Prompt.ask("Enter the length of each segment in seconds", default=30)
    segment_length = int(segment_length_input)  # Cast input to int explicitly

    split_audio(file_path, segment_length)

    console.print(f"[green]Audio splitting complete! Segments created.[/green]")
    log_event(f"Audio splitting complete for {file_path} into {segment_length}-second segments")


if __name__ == "__main__":
    main()
