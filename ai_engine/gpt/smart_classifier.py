from utils.config import config
# ai_engine/gpt/smart_classifier.py

"""
SampleMindAI – Smart Classifier
AI-driven tagging/classification of audio files, using Hermes as primary model.
Fallback to librosa or local CNN if Hermes is unavailable.
"""

import os
from typing import Dict
from rich.console import Console

console = Console()

def tag_audio_hermes(filepath: str) -> Dict[str, str]:
    """
    Tag an audio file using Hermes (Ollama API or local inference).
    Returns dict: {"genre": ..., "mood": ..., "instrument": ...}
    """
    try:
        import requests
        HERMES_API_URL = os.getenv("HERMES_API_URL", "http://localhost:11434/api/generate")
        with open(filepath, "rb") as f:
            files = {'file': (os.path.basename(filepath), f, 'audio/wav')}
            data = {
                "model": config.HERMES_MODEL,
                "task": "audio_tagging"
            }
            response = requests.post(HERMES_API_URL, data=data, files=files, timeout=60)
            response.raise_for_status()
            tags = response.json()
            # Eksempel på forventet Hermes-respons: {"genre": "Techno", "mood": "Dark", "instrument": "Kick"}
            if all(key in tags for key in ("genre", "mood", "instrument")):
                return {k: tags.get(k, "Unknown") for k in ["genre", "mood", "instrument"]}
            else:
                console.print(f"[yellow]Hermes returned incomplete tags: {tags}[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Hermes AI failed: {e}[/yellow]")
    # Fallback
    return tag_audio_librosa(filepath)

def tag_audio_librosa(filepath: str) -> Dict[str, str]:
    """
    Fallback: Use librosa to extract features and classify heuristically.
    """
    try:
        import librosa
        import numpy as np
        y, sr = librosa.load(filepath, sr=None, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        avg_mfcc = np.mean(mfcc, axis=1).tolist()
        # Simple heuristics (kan byttes med ML-modell)
        genre = "Techno" if tempo > 122 else "House" if tempo > 110 else "Unknown"
        mood = "Energetic" if avg_mfcc[0] > 0 else "Chill"
        instrument = "Kick" if "kick" in filepath.lower() else "Loop" if "loop" in filepath.lower() else "Sample"
        return {"genre": genre, "mood": mood, "instrument": instrument}
    except Exception as e:
        console.print(f"[yellow]Librosa fallback failed: {e}[/yellow]")
    # Fallback
    return tag_audio_cnn(filepath)

def tag_audio_cnn(filepath: str) -> Dict[str, str]:
    """
    Final fallback: Use local CNN model (if available).
    """
    try:
        from ai_engine.cnn.cnn_predict import predict_cnn
        return predict_cnn(filepath)
    except Exception as e:
        console.print(f"[red]All AI tagging failed for {filepath}: {e}[/red]")
    # Ultimate fallback
    return {"genre": "Unknown", "mood": "Unknown", "instrument": "Unknown"}

def main():
    """
    Standalone test/debug mode.
    """
    from rich.prompt import Prompt
    test_file = Prompt.ask("Path to audio file for AI-tagging", default="")
    if not os.path.isfile(test_file):
        console.print(f"[red]File not found: {test_file}[/red]")
        return
    tags = tag_audio_hermes(test_file)
    console.print(f"[green]AI Tags:[/green] {tags}")

if __name__ == "__main__":
    main()