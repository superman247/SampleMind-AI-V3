# cli/options/analyzer.py

"""
SampleMindAI – Universal Analyzer
Analyze audio files (single or batch) for key stats and save as .json metadata.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
import wave
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def analyze_wav_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Analyze a WAV file for basic stats.
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
        log_event(f"Analyzer error: {filepath}: {e}")
        return None

def analyze_files(files: List[str]) -> int:
    """Analyze a list of files and save their stats as .json sidecars. Returns count processed."""
    processed = 0
    for f in track(files, description="Analyzing"):
        stats = analyze_wav_file(f)
        if stats:
            json_path = os.path.splitext(f)[0] + ".json"
            with open(json_path, "w") as fp:
                json.dump(stats, fp, indent=2)
            log_event(f"Analyzed: {f} [{stats}]")
            processed += 1
    return processed

def main() -> None:
    """
    CLI entrypoint for universal audio analysis (single or batch).
    """
    console.print("[bold magenta]SampleMindAI – Universal Analyzer[/bold magenta]")
    mode = Prompt.ask("Analyze [1] single file or [2] all in folder?", choices=["1", "2"], default="1")

    if mode == "1":
        file_path = Prompt.ask("Path to audio file")
        if not os.path.isfile(file_path):
            console.print(f"[red]File '{file_path}' does not exist. Aborting.[/red]")
            return
        processed = analyze_files([file_path])
    else:
        folder = Prompt.ask("Folder to analyze", default=config.SAMPLES_DIR)
        if not os.path.isdir(folder):
            console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/red]")
            return
        files = find_all_audio_files(folder, [".wav"])
        if not files:
            console.print(f"[yellow]No .wav files found in {folder}[/yellow]")
            return
        processed = analyze_files(files)

    if processed:
        console.print(f"[green]Analyzed {processed} file(s). Stats saved as .json files.[/green]")
    else:
        console.print("[yellow]No valid files analyzed.[/yellow]")

if __name__ == "__main__":
    main()
