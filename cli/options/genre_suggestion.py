# cli/options/genre_suggestion.py

"""
SampleMindAI – Genre Suggestion
Suggest genres for audio files based on their metadata or content.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json

console = Console()

def suggest_genre(file_path: str) -> str:
    """
    Placeholder function for suggesting a genre for an audio file.
    In the future, this would be based on audio analysis or metadata.
    """
    try:
        json_path = os.path.splitext(file_path)[0] + ".json"
        if not os.path.exists(json_path):
            console.print(f"[yellow]No metadata found for {file_path}. Skipping genre suggestion.[/yellow]")
            return "No metadata available."

        with open(json_path, "r") as f:
            metadata = json.load(f)
        
        # Placeholder: Suggest genre based on some metadata (e.g., genre tag)
        suggested_genre = metadata.get("genre", "Unknown Genre")
        return suggested_genre
    
    except Exception as e:
        console.print(f"[red]Failed to suggest genre for {file_path}: {e}[/red]")
        log_event(f"Failed to suggest genre for {file_path}: {e}")
        return "Error suggesting genre."

def main() -> None:
    """
    CLI entrypoint for suggesting genres for audio files.
    """
    console.print("[bold magenta]SampleMindAI – Genre Suggestion[/bold magenta]")

    file_path = Prompt.ask("Enter the path to the audio file")
    if not file_path or not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    suggested_genre = suggest_genre(file_path)
    console.print(f"[green]Suggested genre: {suggested_genre}[/green]")

    log_event(f"Genre suggestion for {file_path}: {suggested_genre}")

if __name__ == "__main__":
    main()
