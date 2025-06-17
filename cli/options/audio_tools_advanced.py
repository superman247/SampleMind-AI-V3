# cli/options/audio_tools_advanced.py
"""
Advanced Audio Tools: Spectral analysis, harmonic content, pitch contour,
ML-ready feature extraction using librosa + essentia (if available).
"""

import os
from pathlib import Path
from typing import Optional

import numpy as np
import librosa

from rich.console import Console
from rich.prompt import Prompt
from utils.config import get_config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files

console = Console()
config = get_config()


def extract_advanced_features(file_path: Path) -> Optional[dict]:
    try:
        y, sr = librosa.load(file_path, sr=None)

        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y).mean()

        # Pitch and harmony
        pitches, _ = librosa.piptrack(y=y, sr=sr)
        dominant_pitch = np.max(pitches)

        return {
            "spectral_centroid": float(spectral_centroid),
            "spectral_bandwidth": float(spectral_bandwidth),
            "spectral_rolloff": float(spectral_rolloff),
            "zero_crossing_rate": float(zero_crossing_rate),
            "dominant_pitch": float(dominant_pitch)
        }
    except Exception as e:
        console.print(f"[red]Error analyzing {file_path.name}: {e}")
        log_event("audio_analysis_failed", {"file": str(file_path), "error": str(e)})
        return None

def main(debug: bool = False):
    console.rule("[bold magenta]SampleMindAI – Advanced Audio Tools")
    folder = Prompt.ask("Enter path to folder with audio files", default=config["sample_library"])
    folder_path = Path(folder).expanduser()
    if not folder_path.exists():
        console.print("[bold red]Folder does not exist.")
        return

    audio_files = find_all_audio_files(folder_path)
    if not audio_files:
        console.print("[yellow]No audio files found.")
        return

    for path in audio_files:
        console.print(f"\n[bold cyan]Analyzing:[/bold cyan] {path.name}")
        features = extract_advanced_features(path)
        if features:
            for key, value in features.items():
                console.print(f"{key}: {value:.2f}")
            log_event("advanced_features_extracted", {"file": str(path), **features})

if __name__ == "__main__":
    main()
