# utils/file_utils.py

"""
File utilities for SampleMindAI.
"""

import os
from typing import List

def ensure_folder_exists(path: str) -> None:
    """Create folder if it does not exist."""
    os.makedirs(path, exist_ok=True)

def find_all_audio_files(folder_path: str, supported_exts: List[str]) -> List[str]:
    """
    Recursively finds all audio files with supported extensions in a folder.
    """
    result = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in supported_exts):
                result.append(os.path.join(root, filename))
    return result

# Debug/test mode
if __name__ == "__main__":
    print("Testing file_utils...")
    test_dir = "./test_samples"
    ensure_folder_exists(test_dir)
    # Add test logic as needed
