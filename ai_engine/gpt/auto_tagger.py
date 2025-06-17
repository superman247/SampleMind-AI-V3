from utils.config import config
# ai_engine/gpt/auto_tagger.py

from typing import Dict
from rich.console import Console
from rich.progress import track
from utils.file_utils import find_all_audio_files, save_metadata
from core.ai_backend import query_ai

console = Console()

def auto_tag_samples(path: str, backend: str = "hermes") -> None:
    """
    Automatically tags all audio files in the given path using an AI backend.

    Args:
        path (str): Path to the folder containing audio files.
        backend (str): AI backend to use ("hermes" or "openai").
    """
    audio_files = find_all_audio_files(path)
    if not audio_files:
        console.print("[bold red]No audio files found to tag.[/bold red]")
        return

    console.print(f"[bold cyan]Auto-tagging {len(audio_files)} files using {backend}...[/bold cyan]")

    for file in track(audio_files, description="Tagging..."):
        try:
            tags: Dict[str, str] = query_ai(file, backend=backend)

            if isinstance(tags, dict) and "genre" in tags:
                save_metadata(file, tags)
                console.print(f"[green]Tagged:[/green] {file} → {tags}")
            else:
                console.print(f"[red]Invalid AI tags for:[/red] {file}")

        except Exception as e:
            console.print(f"[bold red]Error tagging {file}:[/bold red] {e}")

def main() -> None:
    """
    CLI entrypoint for auto_tag_samples.
    """
    from rich.prompt import Prompt

    path = Prompt.ask("📁 Folder to tag", default=config.SAMPLES_DIR)
    backend = Prompt.ask("🤖 AI backend", choices=["hermes", "openai"], default=config.AI_BACKEND)
    auto_tag_samples(path, backend)

if __name__ == "__main__":
    main()