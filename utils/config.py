# utils/config.py

"""
Centralized configuration for SampleMindAI.
Handles all project paths, environment variables, and AI backend selection.

Usage:
    from utils.config import config
    samples_dir = config.SAMPLES_DIR
    ai_backend = config.AI_BACKEND
"""

import os
from typing import Dict, Any, List

class SampleMindConfig:
    """
    Singleton configuration object for the SampleMindAI project.
    All settings (paths, AI backend, etc) are available as attributes.
    """
    def __init__(self) -> None:
        self.PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.DATA_DIR: str = os.path.join(self.PROJECT_ROOT, "data")
        self.SAMPLES_DIR: str = os.path.join(self.DATA_DIR, "processed_samples")
        self.LOOPS_DIR: str = os.path.join(self.DATA_DIR, "loops")
        self.AUDIO_DIR: str = os.path.join(self.DATA_DIR, "audio")
        self.CACHE_DIR: str = os.path.join(self.PROJECT_ROOT, "cache")
        self.MODELS_DIR: str = os.path.join(self.PROJECT_ROOT, "models")
        self.OUTPUT_DIR: str = os.path.join(self.PROJECT_ROOT, "output")

        # AI backend configuration
        self.AI_BACKEND: str = os.getenv("SAMPLEMIND_AI_BACKEND", "hermes")  # "hermes", "librosa", "fallback_cnn"
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-turbo")
        self.HERMES_MODEL: str = os.getenv("HERMES_MODEL", "hermes-2-pro")
        self.FALLBACK_CNN_MODEL: str = os.path.join(self.MODELS_DIR, "cnn_audio_classifier.h5")

        # Supported audio file formats
        self.SUPPORTED_EXTENSIONS: List[str] = [".wav", ".mp3", ".flac", ".aiff", ".ogg", ".m4a"]

        # Debug/Test mode
        self.DEBUG_MODE: bool = os.getenv("SAMPLEMIND_DEBUG", "0") == "1"

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns the config as a dictionary.
        """
        return self.__dict__

    def print_summary(self) -> None:
        """
        Print all config attributes (for debug).
        """
        print("\n===== SampleMindAI Config =====")
        for k, v in self.as_dict().items():
            print(f"{k}: {v}")
        print("==============================\n")

# Singleton config object for import everywhere
config = SampleMindConfig()

# Debug/test entry point
if __name__ == "__main__":
    config.print_summary()
