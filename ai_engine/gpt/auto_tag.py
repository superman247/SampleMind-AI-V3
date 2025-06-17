from utils.config import config
# ai_engine/gpt/auto_tag.py

from typing import Dict
from rich.console import Console
from rich.progress import track
from utils.file_utils import find_all_audio_files, save_metadata
from core.ai_backend import query_ai

console = Console()

def auto_tag_folder(path: str, backend: str = "hermes") -> None:
    """
    Auto-tags all audio files in the specified folder using an AI backend.

    Args:
        path (str): Path to the folder containing audio files.
        backend (str): AI backend to use ("hermes" or "openai").
    """
    audio_files = find_all_audio_files(path)
    if not audio_files:
        console.print(f"[red]No audio files found in {path}[/red]")
        return

    console.print(f"[cyan]Auto-tagging {len(audio_files)} audio files using {backend}...[/cyan]")

    for file_path in track(audio_files, description="Auto-tagging"):
        try:
            tags: Dict[str, str] = query_ai(file_path, backend=backend)
            if isinstance(tags, dict) and "genre" in tags:
                save_metadata(file_path, tags)
                console.print(f"[green]Tagged:[/green] {file_path} → {tags}")
            else:
                console.print(f"[red]AI returned invalid metadata for:[/red] {file_path}")
        except Exception as error:
            console.print(f"[bold red]Failed to tag {file_path}:[/bold red] {error}")

def main() -> None:
    """
    CLI entry point for auto-tagging.
    """
    from rich.prompt import Prompt

    path = Prompt.ask("📁 Folder to auto-tag", default=config.SAMPLES_DIR)
    backend = Prompt.ask("🤖 Choose AI backend", choices=["hermes", "openai"], default=config.AI_BACKEND)
    auto_tag_folder(path, backend)

if __name__ == "__main__":
    main()