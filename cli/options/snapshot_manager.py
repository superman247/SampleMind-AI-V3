# cli/options/snapshot_manager.py

"""
SampleMindAI – Snapshot Manager
Manage and restore snapshots of the audio library's state (e.g., folder structure, metadata).
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import json
import shutil

console = Console()

def list_snapshots() -> None:
    """
    List all available snapshots in the snapshots directory.
    """
    snapshot_dir = os.path.join(config.OUTPUT_DIR, "snapshots")
    if not os.path.exists(snapshot_dir):
        console.print(f"[red]No snapshots found. Directory '{snapshot_dir}' does not exist.[/]")
        return
    
    snapshot_files = [f for f in os.listdir(snapshot_dir) if f.endswith(".json")]
    if not snapshot_files:
        console.print(f"[yellow]No snapshot files found in {snapshot_dir}[/yellow]")
        return

    console.print(f"[bold cyan]Available snapshots:[/bold cyan]")
    for snapshot in snapshot_files:
        console.print(f"[cyan]{snapshot}[/cyan]")
    log_event(f"Listed available snapshots from {snapshot_dir}")

def restore_snapshot(snapshot_name: str) -> None:
    """
    Restore a snapshot from the snapshot folder.
    """
    snapshot_path = os.path.join(config.OUTPUT_DIR, "snapshots", f"{snapshot_name}.json")
    if not os.path.exists(snapshot_path):
        console.print(f"[red]Snapshot '{snapshot_name}' not found. Aborting.[/]")
        return
    
    with open(snapshot_path, "r") as f:
        snapshot_data = json.load(f)
    
    console.print(f"[cyan]Restoring snapshot: {snapshot_name} from {snapshot_path}[/cyan]")

    # Placeholder logic: Simulate restoring the snapshot by copying files back (this can be expanded)
    snapshot_folder = os.path.join(config.SAMPLES_DIR, snapshot_name)
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    # Just copying files from the snapshot (this logic can be expanded)
    for file in snapshot_data.get("folder_contents", []):
        # Placeholder: Move files back to the original folder
        shutil.copy(os.path.join(config.SAMPLES_DIR, file), snapshot_folder)
        console.print(f"[cyan]Restored: {file}[/cyan]")

    log_event(f"Restored snapshot {snapshot_name} from {snapshot_path}")

def delete_snapshot(snapshot_name: str) -> None:
    """
    Delete a snapshot file.
    """
    snapshot_path = os.path.join(config.OUTPUT_DIR, "snapshots", f"{snapshot_name}.json")
    if os.path.exists(snapshot_path):
        os.remove(snapshot_path)
        console.print(f"[green]Snapshot {snapshot_name} deleted successfully.[/green]")
        log_event(f"Deleted snapshot {snapshot_name}")
    else:
        console.print(f"[red]Snapshot '{snapshot_name}' not found. Aborting.[/]")

def main() -> None:
    """
    CLI entrypoint for managing snapshots.
    """
    console.print("[bold magenta]SampleMindAI – Snapshot Manager[/bold magenta]")

    action = Prompt.ask("What would you like to do?", choices=["1", "2", "3"], default="1")

    if action == "1":
        list_snapshots()

    elif action == "2":
        snapshot_name = Prompt.ask("Enter the snapshot name to restore")
        restore_snapshot(snapshot_name)

    elif action == "3":
        snapshot_name = Prompt.ask("Enter the snapshot name to delete")
        delete_snapshot(snapshot_name)

    log_event(f"Snapshot management action completed")

if __name__ == "__main__":
    main()
