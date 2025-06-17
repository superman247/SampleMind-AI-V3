# cli/options/ask_hermes.py

"""
SampleMindAI – Ask Hermes
Interactively query the Hermes AI model for metadata or creative suggestions about an audio file.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
from typing import Dict, Optional, Any
from rich.console import Console
from rich.prompt import Prompt

from utils.config import config
from utils.logger import log_event
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes

console = Console()

def ask_hermes_about_file(audio_path: str, question: str = "") -> Optional[Dict[str, Any]]:
    """
    Ask Hermes for information or tags about an audio file.
    If no question is given, defaults to tagging (genre/mood/instrument).
    """
    try:
        if not question.strip():
            # Default: Tagging
            console.print(f"[cyan]Querying Hermes for genre/mood/instrument of {os.path.basename(audio_path)}...[/cyan]")
            tags = tag_file_with_hermes(audio_path)
            log_event(f"Hermes tag: {audio_path} [{tags}]")
            return tags
        else:
            # Try to import ask_hermes_custom_prompt if available
            try:
                from ai_engine.hermes.hermes_tagger import ask_hermes_custom_prompt  # type: ignore
                answer = ask_hermes_custom_prompt(audio_path, question)
                log_event(f"Hermes Q&A: {audio_path} [{question}] => {answer}")
                return {"question": question, "answer": answer}
            except ImportError:
                console.print("[yellow]Custom question support is not implemented in Hermes yet.[/yellow]")
                log_event(f"ask_hermes_custom_prompt missing for: {audio_path} [{question}]")
                return {"question": question, "answer": "Not implemented in Hermes."}
            except AttributeError:
                console.print("[yellow]Custom question support is not implemented in Hermes yet.[/yellow]")
                log_event(f"ask_hermes_custom_prompt attribute missing: {audio_path} [{question}]")
                return {"question": question, "answer": "Not implemented in Hermes."}
    except Exception as e:
        console.print(f"[red]Failed to query Hermes: {e}[/]")
        log_event(f"Ask Hermes failed: {audio_path}: {e}")
        return None

def main() -> None:
    """
    CLI entrypoint for querying Hermes AI about an audio file.
    """
    console.print("[bold magenta]SampleMindAI – Ask Hermes[/bold magenta]")
    file_path = Prompt.ask("Path to audio file")
    if not os.path.isfile(file_path):
        console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
        return

    mode = Prompt.ask("Ask for [1] metadata/tags or [2] custom question?", choices=["1", "2"], default="1")
    if mode == "1":
        tags = ask_hermes_about_file(file_path)
        if tags:
            console.print(f"[green]Hermes tags: {tags}[/green]")
    else:
        question = Prompt.ask("Enter your question for Hermes about this audio file")
        result = ask_hermes_about_file(file_path, question)
        if result:
            console.print(f"[green]Hermes response: {result.get('answer', result)}[/green]")

    console.print("[bold green]Hermes query complete![/bold green]")

if __name__ == "__main__":
    main()
