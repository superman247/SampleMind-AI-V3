# cli/options/analyze_audio_stats.py

"""
SampleMindAI – Analyze Audio Stats
Batch analyzes all audio files in a folder for key stats and saves as .json sidecar files.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
import wave
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists

console = Console()

def analyze_wav_stats(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Analyze a WAV file for key stats.
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

def analyze_audio_stats(folder: str) -> List[Dict[str, Any]]:
    """
    Analyze all supported audio files in the given folder.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, [".wav"])  # Focus on .wav for universal support
    if not audio_files:
        console.print(f"[yellow]No .wav files found in {folder}[/]")
        return []

    console.print(f"[bold cyan]Analyzing {len(audio_files)} files in {folder}...[/bold cyan]")
    results = []

    for audio_path in track(audio_files, description="Analyzing"):
        stats = analyze_wav_stats(audio_path)
        if stats:
            # Save per-file stats as .json
            json_path = os.path.splitext(audio_path)[0] + ".json"
            with open(json_path, "w") as f:
                json.dump(stats, f, indent=2)
            results.append({"path": audio_path, **stats})
            log_event(f"Analyzed audio stats: {audio_path} [{stats}]")

    return results

def main() -> None:
    """
    CLI entrypoint for batch analyzing audio stats in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Analyze Audio Stats[/bold magenta]")
    folder = Prompt.ask("Folder to analyze", default=config.SAMPLES_DIR)
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    results = analyze_audio_stats(folder)
    if results:
        console.print(f"[green]Analyzed {len(results)} audio files. Stats saved as .json files.[/green]")
    else:
        console.print("[yellow]No valid audio files analyzed.[/yellow]")

if __name__ == "__main__":
    main()
