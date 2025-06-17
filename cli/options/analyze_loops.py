# cli/options/analyze_loops.py

"""
SampleMindAI – Analyze Loops Module
Batch analyzes all audio loops in a folder, extracts key features, and saves stats as .json.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
import wave
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def analyze_wav_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Analyze a WAV file and extract features.
    Returns a dictionary with stats, or None on error.
    """
    try:
        with wave.open(filepath, "rb") as wf:
            return {
                "sample_rate": wf.getframerate(),
                "channels": wf.getnchannels(),
                "sample_width": wf.getsampwidth(),
                "frame_count": wf.getnframes(),
                "duration_sec": wf.getnframes() / float(wf.getframerate()),
            }
    except Exception as e:
        console.print(f"[red]Failed to analyze {filepath}: {e}[/]")
        log_event(f"Failed to analyze {filepath}: {e}")
        return None

def analyze_loop_files(folder: str) -> List[Dict[str, Any]]:
    """
    Analyze all supported audio loops in the given folder.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, [".wav"])  # Loops are usually WAV, can expand as needed
    if not audio_files:
        console.print(f"[yellow]No .wav loop files found in {folder}[/]")
        return []

    console.print(f"[bold cyan]Analyzing {len(audio_files)} loop files in {folder}...[/bold cyan]")
    results = []

    for audio_path in track(audio_files, description="Analyzing"):
        stats = analyze_wav_file(audio_path)
        if stats:
            # Save per-file stats as .json
            json_path = os.path.splitext(audio_path)[0] + ".json"
            with open(json_path, "w") as f:
                json.dump(stats, f, indent=2)
            results.append({"path": audio_path, **stats})
            log_event(f"Analyzed loop: {audio_path} [{stats}]")

    return results

def main() -> None:
    """
    CLI entrypoint for batch analyzing loops in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Analyze Loops[/bold magenta]")
    folder = Prompt.ask("Folder to analyze", default=config.LOOPS_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    results = analyze_loop_files(folder)
    if results:
        console.print(f"[green]Analyzed {len(results)} loops. Stats saved as .json files.[/green]")
    else:
        console.print("[yellow]No valid loop files analyzed.[/yellow]")

if __name__ == "__main__":
    main()
