# cli/options/initializer.py

"""
SampleMindAI – Initializer
Set up the SampleMindAI project by initializing necessary configurations and file structures.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os

console = Console()

def initialize_project_structure() -> None:
    """
    Placeholder function for initializing project structure.
    Creates necessary directories or config files (e.g., for the sample library, cache, etc.).
    """
    required_dirs = [
        config.SAMPLES_DIR,
        config.OUTPUT_DIR,
        config.CACHE_DIR,
        config.MODELS_DIR
    ]

    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            console.print(f"[cyan]Created directory: {directory}[/cyan]")
            log_event(f"Created directory: {directory}")
        else:
            console.print(f"[green]Directory already exists: {directory}[/green]")
    
def main() -> None:
    """
    CLI entrypoint for initializing the SampleMindAI project.
    """
    console.print("[bold magenta]SampleMindAI – Initializer[/bold magenta]")
    
    action = Prompt.ask(
        "Initialize project structure? [Y/N]",
        choices=["Y", "N"],
        default="Y"
    )

    if action.lower() == "y":
        initialize_project_structure()
        console.print(f"[green]Project structure initialized successfully![/green]")
        log_event("Project structure initialization complete")
    else:
        console.print(f"[yellow]Aborted initialization.[/yellow]")

if __name__ == "__main__":
    main()
