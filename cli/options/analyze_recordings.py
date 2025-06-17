# cli/options/analyze_recordings.py

"""
SampleMindAI – Analyze Recordings CLI
Extracts audio features from all recordings in a folder and saves as .json.
"""

import os
import json
from typing import List, Dict, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

from utils.config import config
import librosa

console = Console()

FEATURES = [
    "duration", "sample_rate", "rms", "zero_crossings", "mfcc_mean"
]


def get_audio_files(folder: str, extensions: List[str]) -> List[str]:
    """Recursively find all audio files in a folder."""
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if any(f.lower().endswith(ext) for ext in extensions):
                files.append(os.path.join(root, f))
    return files


def extract_audio_features(filepath: str) -> Dict[str, Optional[float]]:
    """Extract audio features from one file."""
    try:
        y, sr = librosa.load(filepath, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)
        rms = float(librosa.feature.rms(y=y).mean())
        zero_crossings = int(librosa.zero_crossings(y).sum())
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = float(mfcc.mean())
        return {
            "duration": duration,
            "sample_rate": sr,
            "rms": rms,
            "zero_crossings": zero_crossings,
            "mfcc_mean": mfcc_mean,
        }
    except Exception as e:
        console.print(f"[red]Failed to extract features from {filepath}: {e}[/red]")
        return {k: None for k in FEATURES}


def analyze_recordings_folder(folder: str, debug: bool = False) -> None:
    """Analyze all recordings in a folder and write feature .json files."""
    files = get_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not files:
        console.print(f"[red]No audio files found in {folder}[/red]")
        return

    for f in track(files, description="Analyzing recordings..."):
        features = extract_audio_features(f)
        json_path = os.path.splitext(f)[0] + "_features.json"
        try:
            with open(json_path, "w") as fp:
                json.dump(features, fp, indent=2)
            if debug:
                console.print(f"[green]Features for {f}: {features}[/green]")
        except Exception as e:
            console.print(f"[red]Failed to save features for {f}: {e}[/red]")

    console.print("[bold green]Recording analysis complete.[/bold green]")


# CLI/test entry point
if __name__ == "__main__":
    folder = Prompt.ask(
        "Folder to analyze recordings",
        default=config.AUDIO_DIR
    )
    analyze_recordings_folder(folder, debug=True)
