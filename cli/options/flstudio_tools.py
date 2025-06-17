# cli/options/flstudio_tools.py

"""
SampleMindAI – FL Studio Tools
Tools for integrating with FL Studio (e.g., managing projects, importing files).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os

console = Console()

def list_flp_projects(folder: str) -> None:
    """
    Placeholder function for listing FL Studio projects (.flp files) in a folder.
    """
    flp_files = [f for f in os.listdir(folder) if f.lower().endswith(".flp")]
    if flp_files:
        console.print(f"[green]Found the following FLP projects:[/green]")
        for flp in flp_files:
            console.print(f"[cyan]{flp}[/cyan]")
        log_event(f"Listed {len(flp_files)} FLP files in {folder}")
    else:
        console.print(f"[yellow]No FLP projects found in {folder}[/yellow]")
        log_event(f"No FLP files found in {folder}")

def main() -> None:
    """
    CLI entrypoint for FL Studio tools.
    """
    console.print("[bold magenta]SampleMindAI – FL Studio Tools[/bold magenta]")

    folder = Prompt.ask("Enter the folder to list FLP projects", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    list_flp_projects(folder)

    console.print("[green]FL Studio project listing complete![/green]")
    log_event(f"FL Studio project listing complete for {folder}")

if __name__ == "__main__":
    main()
