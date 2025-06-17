from utils.config import config
# ai_engine/gpt/ai_reanalyzer.py

from typing import Dict
from rich.console import Console
from rich.prompt import Confirm
from utils.file_utils import find_all_audio_files, save_metadata
from core.ai_backend import query_ai

console = Console()

def reanalyze_tags(path: str, backend: str = "hermes") -> None:
    """
    Reanalyzes and replaces tags for all audio files in the given path using the AI backend.

    Args:
        path (str): Path to the folder containing audio files.
        backend (str): AI backend to use for tagging ("hermes", "openai").
    """
    audio_files = find_all_audio_files(path)
    if not audio_files:
        console.print("[bold red]No audio files found.[/bold red]")
        return

    console.print(f"[bold cyan]Reanalyzing tags using {backend}...[/bold cyan]")

    for file in audio_files:
        if Confirm.ask(f"Reanalyze and overwrite tags for [yellow]{file}[/yellow]?", default=True):
            tags: Dict[str, str] = query_ai(file, backend=backend)

            if isinstance(tags, dict) and "genre" in tags:
                save_metadata(file, tags)
                console.print(f"[green]Reanalyzed:[/green] {file} → {tags}")
            else:
                console.print(f"[red]Failed to generate valid tags for:[/red] {file}")

def main() -> None:
    """
    Main CLI entrypoint for AI reanalyzer module.
    """
    from rich.prompt import Prompt
    from utils.config import config.SAMPLES_DIR, config.AI_BACKEND

    path = Prompt.ask("📁 Folder to reanalyze", default=config.SAMPLES_DIR)
    backend = Prompt.ask("🤖 AI backend", choices=["hermes", "openai"], default=config.AI_BACKEND)
    reanalyze_tags(path, backend)

if __name__ == "__main__":
    main()