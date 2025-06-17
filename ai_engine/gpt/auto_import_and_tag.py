from utils.config import config
# cli/options/auto_import_and_tag.py

from typing import Dict
from core.ai_backend import query_ai
from utils.file_utils import find_all_audio_files, save_metadata
from rich.prompt import Prompt
from rich.console import Console

console = Console()

def import_and_tag(path: str, backend: str) -> None:
    """
    Scans a folder for audio files, uses the AI backend to classify each file,
    and saves metadata for each one.
    """
    files = find_all_audio_files(path)
    if not files:
        console.print(f"[red]No audio files found in {path}[/red]")
        return

    for file in files:
        tags: Dict[str, str] = query_ai(file, backend)
        if not isinstance(tags, dict):
            console.print(f"[yellow]Warning:[/yellow] Invalid metadata returned for {file}")
            continue

        save_metadata(file, tags)
        console.print(f"[green]Tagged:[/green] {file} -> {tags}")

def main() -> None:
    """
    Main entry point for CLI option.
    """
    path = Prompt.ask("\U0001F4C2 Folder to auto-import and tag", default=config.SAMPLES_DIR)
    backend = Prompt.ask("\U0001F916 AI Backend", choices=["hermes", "openai"], default=config.AI_BACKEND)
    import_and_tag(path, backend)

if __name__ == "__main__":
    main()