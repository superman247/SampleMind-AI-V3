from utils.config import config
# core/analyzer.py

"""
Shared analyzer utilities for SampleMind CLI tools.

Provides functions to:
- Find audio files
- Compute duration
- Validate metadata tags
"""

from pathlib import Path
from typing import List, Dict
import json
import librosa

VALID_FIELDS: set[str] = {"genre", "mood", "instrument"}
config.SUPPORTED_EXTENSIONS: List[str] = [".wav", ".aiff", ".flac", ".mp3"]


def find_audio_files(directory: Path) -> List[Path]:
    """Recursively find supported audio files in a directory."""
    return [
        f for f in directory.rglob("*")
        if f.suffix.lower() in config.SUPPORTED_EXTENSIONS and f.is_file()
    ]


def get_json_path(file_path: Path) -> Path:
    """Return corresponding .json metadata path for a given audio file."""
    return file_path.with_suffix(".json")


def get_audio_duration(file_path: Path) -> float:
    """Get duration of audio file in seconds."""
    try:
        return float(librosa.get_duration(path=str(file_path)))  # type: ignore
    except Exception:
        return 0.0


def is_valid_metadata(json_path: Path, debug: bool = False) -> bool:
    """
    Check if a JSON metadata file contains all valid tags.
    """
    if not json_path.exists():
        return False
    try:
        with json_path.open("r", encoding="utf-8") as f:
            tags: Dict[str, str] = json.load(f)
        return all(
            key in tags and tags[key].strip().lower() not in ("", "unknown")
            for key in VALID_FIELDS
        )
    except Exception:
        return False