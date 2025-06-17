from utils.config import config
# ai_engine/cnn/cnn_predict.py

"""
SampleMindAI – CNN Audio Classifier
This module provides functions to classify audio files using a pre-trained CNN model.
"""

from ai_engine.cnn.cnn_model import classify_audio_file, load_model
from typing import Dict
from rich.console import Console
import os

console = Console()

# Dynamisk path til modellen fra config – så du slipper hardkoding
MODEL_PATH = config.FALLBACK_CNN_MODEL
MODEL = None

def get_model():
    """Lazy-load model only once."""
    global MODEL
    if MODEL is None:
        if not os.path.isfile(MODEL_PATH):
            console.print(f"[red]CNN model not found at {MODEL_PATH}![/red]")
            return None
        MODEL = load_model(MODEL_PATH)
    return MODEL

def predict_cnn(filepath: str) -> Dict[str, str]:
    """
    Classify a single audio file using the pre-trained CNN model.
    Returns dict: {"genre": ..., "mood": ..., "instrument": ...}
    """
    model = get_model()
    if model is None:
        return {"genre": "Unknown", "mood": "Unknown", "instrument": "Unknown"}
    try:
        return classify_audio_file(model, filepath)
    except Exception as e:
        console.print(f"[red]Error classifying {filepath}: {e}[/red]")
        return {"genre": "Unknown", "mood": "Unknown", "instrument": "Unknown"}

# Eksempel/test (kan slettes i produksjon)
if __name__ == "__main__":
    from rich.prompt import Prompt
    fpath = Prompt.ask("Path to audio file")
    tags = predict_cnn(fpath)
    print(tags)