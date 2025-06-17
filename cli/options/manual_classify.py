# cli/options/manual_classify.py

"""
SampleMindAI – Manual Classify
Manually classify audio files by assigning metadata tags like genre, mood, and instrument.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def classify_audio_file(file_path: str, genre: str, mood: str, instrument: str) -> None:
    """
    Placeholder function for manually classifying an audio file.
    This would save the metadata in a .json file.
    """
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    # Save metadata as a JSON file
    metadata = {
        "genre": genre,
        "mood": mood,
        "instrument": instrument
    }
    
    json_path = os.path.splitext(file_path)[0] + ".json"
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=2)

    console.print(f"[cyan]Classified {file_path} with genre: {genre}, mood: {mood}, instrument: {instrument}[/cyan]")
    log_event(f"Classified {file_path} with genre: {genre}, mood: {mood}, instrument: {instrument}")

def main() -> None:
    """
    CLI entrypoint for manually classifying an audio file.
    """
    console.print("[bold magenta]SampleMindAI – Manual Classify[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    genre = Prompt.ask("Enter the genre for this file", default="Unknown")
    mood = Prompt.ask("Enter the mood for this file", default="Unknown")
    instrument = Prompt.ask("Enter the instrument for this file", default="Unknown")

    classify_audio_file(file_path, genre, mood, instrument)

    console.print(f"[green]Manual classification complete! Metadata saved.[/green]")
    log_event(f"Manual classification complete for {file_path}")

if __name__ == "__main__":
    main()
