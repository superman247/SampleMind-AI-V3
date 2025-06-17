# cli/options/delete_duplicates.py

"""
SampleMindAI – Delete Duplicates
Detect and remove duplicate audio files based on filename, size, or hash.
Future functionality; currently includes a placeholder.
"""

from rich.console import Console
from rich.prompt import Prompt
from utils.config import config
from utils.logger import log_event
import os
import hashlib

console = Console()

def get_file_hash(file_path: str) -> str:
    """
    Generates a hash for a file to detect duplicates. Uses SHA256 by default.
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def delete_duplicate_files(folder: str) -> None:
    """
    Detects and deletes duplicate files in a folder.
    Placeholder for future implementation with real duplicate detection.
    """
    seen_files = {}
    duplicates = []
    
    # Placeholder logic: checking for duplicates based on file hash
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if not file_path.lower().endswith(tuple(config.SUPPORTED_EXTENSIONS)):
                continue

            file_hash = get_file_hash(file_path)
            if file_hash in seen_files:
                duplicates.append(file_path)
                os.remove(file_path)
                log_event(f"Deleted duplicate: {file_path}")
            else:
                seen_files[file_hash] = file_path
    
    if not duplicates:
        console.print(f"[green]No duplicates found in {folder}[/green]")
    else:
        console.print(f"[green]Deleted {len(duplicates)} duplicate file(s) from {folder}[/green]")

def main() -> None:
    """
    CLI entrypoint for deleting duplicate files in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Delete Duplicates[/bold magenta]")

    folder = Prompt.ask("Folder to check for duplicates", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
        return

    delete_duplicate_files(folder)

    console.print("[green]Duplicate deletion complete![/green]")
    log_event(f"Duplicate deletion complete for folder: {folder}")

if __name__ == "__main__":
    main()
