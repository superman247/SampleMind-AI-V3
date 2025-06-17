# cli/options/custom_import_samples.py

"""
SampleMindAI – Custom Import Samples Module
Custom workflow for importing and organizing samples/loops.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
from typing import List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def custom_import_samples(
    source_folder: str,
    destination_folder: str,
    use_subfolders: bool = True,
    prompt_for_tags: bool = False
) -> List[str]:
    """
    Custom import: Copies audio files from source to destination, optionally organizing by tags or subfolders.
    Returns a list of imported file paths.
    """
    ensure_folder_exists(destination_folder)
    files = find_all_audio_files(source_folder, config.SUPPORTED_EXTENSIONS)
    if not files:
        console.print(f"[yellow]No audio files found in {source_folder}[/yellow]")
        return []

    imported_files = []
    console.print(f"[bold cyan]Importing {len(files)} files from {source_folder} to {destination_folder}...[/bold cyan]")

    for src_file in track(files, description="Importing"):
        rel_path = os.path.relpath(src_file, source_folder) if use_subfolders else os.path.basename(src_file)
        dest_path = os.path.join(destination_folder, rel_path)
        dest_dir = os.path.dirname(dest_path)
        ensure_folder_exists(dest_dir)
        try:
            # Copy file (overwrite if exists)
            with open(src_file, "rb") as fsrc, open(dest_path, "wb") as fdst:
                fdst.write(fsrc.read())
            imported_files.append(dest_path)
            log_event(f"Custom import: {src_file} → {dest_path}")
            # Optional: prompt for tags and save .json
            if prompt_for_tags:
                genre = Prompt.ask(f"Genre for {os.path.basename(src_file)}", default="")
                mood = Prompt.ask(f"Mood for {os.path.basename(src_file)}", default="")
                instrument = Prompt.ask(f"Instrument for {os.path.basename(src_file)}", default="")
                tags = {"genre": genre, "mood": mood, "instrument": instrument}
                json_path = os.path.splitext(dest_path)[0] + ".json"
                with open(json_path, "w") as fjson:
                    import json
                    json.dump(tags, fjson, indent=2)
                log_event(f"Manual tags for {dest_path}: {tags}")
        except Exception as e:
            console.print(f"[red]Failed to import {src_file}: {e}[/]")
            log_event(f"Import error for {src_file}: {e}")

    return imported_files

def main() -> None:
    """
    CLI entrypoint for custom import workflow.
    """
    console.print("[bold magenta]SampleMindAI – Custom Import Samples[/bold magenta]")
    source_folder = Prompt.ask("Source folder to import from", default=config.SAMPLES_DIR)
    if not os.path.isdir(source_folder):
        console.print(f"[red]Source folder '{source_folder}' does not exist. Aborting.[/red]")
        return

    destination_folder = Prompt.ask("Destination folder for imported files", default=config.SAMPLES_DIR)
    use_subfolders = Confirm.ask("Preserve subfolder structure?", default=True)
    prompt_for_tags = Confirm.ask("Prompt for tags on each import?", default=False)

    imported = custom_import_samples(
        source_folder=source_folder,
        destination_folder=destination_folder,
        use_subfolders=use_subfolders,
        prompt_for_tags=prompt_for_tags,
    )
    if imported:
        console.print(f"[green]Imported {len(imported)} files successfully![/green]")
    else:
        console.print("[yellow]No files imported.[/yellow]")

if __name__ == "__main__":
    main()
