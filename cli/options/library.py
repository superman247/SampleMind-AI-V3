# cli/options/library.py
"""
SampleMindAI – Central library manager for samples and loops.
Future support for GUI/plugin and full metadata control.
"""

import json
from pathlib import Path
from typing import Dict

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

from utils.config import get_config
from utils.file_utils import find_all_audio_files
from utils.logger import log_event

console = Console()
config = get_config()

LIBRARY_PATH = config["sample_library"]
META_PATH = "data/library_metadata.json"

def load_metadata() -> Dict[str, dict]:
    try:
        with open(META_PATH, "r") as f:
            return json.load(f)
    except Exception:
        console.print("[bold red]Invalid metadata file. Rebuilding.")
    return {}

def save_metadata(data: Dict[str, dict]):
    Path(META_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(META_PATH, "w") as f:
        json.dump(data, f, indent=2)

def scan_library() -> Dict[str, dict]:
    console.print("[cyan]Scanning audio library for metadata...[/cyan]")
    library = {}
    files = find_all_audio_files(str(LIBRARY_PATH), [".wav", ".mp3", ".flac", ".aiff"])
    for path_str in files:
        path = Path(path_str)
        key = str(path.relative_to(Path(LIBRARY_PATH)))
        library[key] = {
            "filename": path.name,
            "path": str(path),
            "size_kb": round(path.stat().st_size / 1024, 1)
        }
    return library

def display_library(data: Dict[str, dict]):
    table = Table(title="Sample Library")
    table.add_column("Filename", style="cyan")
    table.add_column("Size (KB)", justify="right")
    for entry in data.values():
        table.add_row(entry["filename"], str(entry["size_kb"]))
    console.print(table)

def main(debug: bool = False):
    console.rule("[bold blue]SampleMindAI – Library Manager")
    library = load_metadata()

    while True:
        console.print("\n[1] Scan and rebuild library\n[2] View current library\n[3] Export to JSON\n[0] Exit")
        choice = IntPrompt.ask("Choose an option", default=0)

        if choice == 1:
            library = scan_library()
            save_metadata(library)
            log_event("library_scanned", {"items": len(library)})
            console.print(f"[green]Library updated with {len(library)} files.")

        elif choice == 2:
            if not library:
                library = load_metadata()
            display_library(library)

        elif choice == 3:
            export_path = Prompt.ask("Enter export path", default="library_export.json")
            try:
                with open(str(export_path), "w") as f:
                    json.dump(library, f, indent=2)
                console.print(f"[green]Exported metadata to:[/green] {export_path}")
                log_event("library_exported", {"export_path": str(export_path)})
            except Exception as e:
                console.print(f"[red]Failed to export: {e}")

        elif choice == 0:
            break

if __name__ == "__main__":
    main()
