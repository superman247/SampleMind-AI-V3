# cli/options/auto_import_and_tag.py

"""
SampleMindAI – Auto Import & Tag
Import audio files and automatically tag them using the selected AI model.
"""

from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
from utils.metadata_utils import save_metadata  # Correct import for save_metadata
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn
import os

console = Console()

def auto_import_and_tag(file_path: str, ai_backend: str, supported_exts: list) -> None:
    """
    Import an audio file and automatically tag it using the selected AI backend.
    """
    if not any(file_path.endswith(ext) for ext in supported_exts):
        console.print(f"[red]File '{file_path}' is not supported. Skipping.[/red]")
        return
    
    console.print(f"[cyan]Importing and tagging: {file_path}[/cyan]")
    log_event(f"Importing and tagging: {file_path}")
    
    # Select the AI backend for tagging
    if ai_backend == "hermes":
        tags = tag_file_with_hermes(file_path)
    else:
        tags = tag_file_with_cnn(file_path)

    if tags and all(v and str(v).lower() not in {"", "unknown", "none"} for v in tags.values()):
        save_metadata(file_path, tags, supported_exts)  # Make sure to pass supported_exts
        console.print(f"[green]Successfully tagged and saved metadata for {file_path}[/green]")
    else:
        console.print(f"[red]Failed to tag or invalid tags for {file_path}[/red]")
        log_event(f"Failed to tag {file_path} with valid metadata")

def main() -> None:
    """
    CLI entrypoint for importing and tagging audio files.
    """
    console.print("[bold magenta]SampleMindAI – Auto Import & Tag[/bold magenta]")
    
    ai_backend = Prompt.ask("Choose AI backend", choices=["hermes", "cnn"], default="hermes")
    folder = Prompt.ask("Enter the folder containing audio files", default=config.SAMPLES_DIR)
    
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    for file in track(os.listdir(folder), description="Importing and tagging files..."):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            auto_import_and_tag(file_path, ai_backend, supported_exts=config.SUPPORTED_EXTENSIONS)

    console.print("[green]Auto Import & Tagging process complete![/green]")
    log_event(f"Auto Import & Tagging process complete for folder: {folder}")

if __name__ == "__main__":
    main()
