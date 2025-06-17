# cli/options/analyze_favorites.py

"""
SampleMindAI – Analyze Favorites
Analyze all bookmarked/favorite audio files for key stats and save as .json metadata.
Config-driven, Pylance-clean, robust error handling, and Rich CLI UX.
"""

import os
import json
import wave
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import track

from utils.config import config
from utils.logger import log_event

BOOKMARKS_FILE = os.path.join(config.OUTPUT_DIR, "bookmarked_samples.json")
console = Console()

def load_bookmarks() -> List[str]:
    """Load the list of bookmarked file paths."""
    if not os.path.isfile(BOOKMARKS_FILE):
        return []
    try:
        with open(BOOKMARKS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

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

def analyze_favorites() -> List[Dict[str, Any]]:
    """Analyze all bookmarked WAV files and save their stats as .json."""
    files = load_bookmarks()
    wav_files = [f for f in files if f.lower().endswith(".wav")]
    if not wav_files:
        console.print(f"[yellow]No bookmarked .wav files found.[/yellow]")
        return []

    console.print(f"[bold cyan]Analyzing {len(wav_files)} favorite WAV files...[/bold cyan]")
    results = []
    for f in track(wav_files, description="Analyzing favorites"):
        stats = analyze_wav_stats(f)
        if stats:
            json_path = os.path.splitext(f)[0] + ".json"
            with open(json_path, "w") as fp:
                json.dump(stats, fp, indent=2)
            results.append({"path": f, **stats})
            log_event(f"Analyzed favorite: {f} [{stats}]")
    return results

def main() -> None:
    """
    CLI entrypoint for analyzing all favorite/bookmarked files.
    """
    console.print("[bold magenta]SampleMindAI – Analyze Favorites[/bold magenta]")
    results = analyze_favorites()
    if results:
        console.print(f"[green]Analyzed {len(results)} favorites. Stats saved as .json files.[/green]")
    else:
        console.print("[yellow]No valid favorites analyzed.[/yellow]")

if __name__ == "__main__":
    main()
