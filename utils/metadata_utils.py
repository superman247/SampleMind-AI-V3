# utils/metadata_utils.py

"""
SampleMindAI – Metadata Utilities
Utility functions for managing and saving metadata for audio files.
"""

import json
import os
from utils.config import config
from utils.logger import log_event

def save_metadata(file_path: str, metadata: dict, supported_exts: list) -> None:
    """
    Save metadata to a .json file corresponding to the audio file.
    
    Args:
        file_path (str): The path to the audio file.
        metadata (dict): The metadata to save (e.g., genre, mood, instrument).
        supported_exts (list): The list of supported file extensions.
    """
    if not any(file_path.endswith(ext) for ext in supported_exts):
        raise ValueError(f"File '{file_path}' is not a supported type.")
    
    # Save metadata as a .json file
    json_path = os.path.splitext(file_path)[0] + ".json"
    try:
        with open(json_path, "w") as json_file:
            json.dump(metadata, json_file, indent=2)
        log_event(f"Saved metadata for {file_path} to {json_path}")
    except Exception as e:
        raise Exception(f"Failed to save metadata for {file_path}: {e}")
    
    # Optionally, log the saved metadata (for debug purposes)
    log_event(f"Metadata for {file_path}: {metadata}")
    
def load_metadata(file_path: str) -> dict:
    """
    Load metadata from the .json file corresponding to an audio file.
    
    Args:
        file_path (str): The path to the audio file.
    
    Returns:
        dict: The loaded metadata.
    """
    json_path = os.path.splitext(file_path)[0] + ".json"
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Metadata file '{json_path}' not found.")
    
    try:
        with open(json_path, "r") as json_file:
            metadata = json.load(json_file)
        return metadata
    except Exception as e:
        raise Exception(f"Failed to load metadata from {json_path}: {e}")

def update_metadata(file_path: str, new_metadata: dict) -> None:
    """
    Update existing metadata for an audio file.
    
    Args:
        file_path (str): The path to the audio file.
        new_metadata (dict): The new metadata to merge into the existing metadata.
    """
    metadata = load_metadata(file_path)
    metadata.update(new_metadata)
    
    # Save the updated metadata back to the file
    save_metadata(file_path, metadata, supported_exts=config.SUPPORTED_EXTENSIONS)
    log_event(f"Updated metadata for {file_path} with {new_metadata}")
