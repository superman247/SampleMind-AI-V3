from utils.config import config
# core/project_mapper.py

import os
from pathlib import Path
from typing import List, Dict

# Path to the root project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_all_files_in_project() -> List[str]:
    """
    Recursively fetch all files in the project directory, starting from PROJECT_ROOT.
    """
    all_files: List[str] = []  # Explicitly define the type of the list
    for root, _, files in os.walk(PROJECT_ROOT):  # Ignore 'dirs' since it's unused
        for file in files:
            all_files.append(os.path.relpath(os.path.join(root, file), PROJECT_ROOT))
    return all_files

def map_files_by_extension(extension: str) -> List[str]:
    """
    Map files by a specific extension in the project directory.
    
    Args:
        extension (str): The file extension to search for (e.g., '.py', '.txt').
    
    Returns:
        list: A list of file paths matching the given extension.
    """
    return [file for file in get_all_files_in_project() if file.endswith(extension)]

def get_project_info() -> Dict[str, str | List[str]]:
    """
    Return basic information about the project: name, root path, and file count.
    """
    all_files = get_all_files_in_project()
    return {
        "project_name": PROJECT_ROOT.name,
        "root_path": str(PROJECT_ROOT),
        "file_count": str(len(all_files)),  # Ensure the file count is a string
        "files": all_files  # `List[str]` is expected, so return the list of files
    }