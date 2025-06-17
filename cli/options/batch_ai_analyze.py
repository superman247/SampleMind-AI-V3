# cli/options/batch_ai_analyze.py

"""
SampleMindAI – Batch AI Analyze Module
Batch analyzes all audio files in a folder using Hermes AI (primary) or fallback.
Saves/prints tags, supports config, robust error handling, and Pylance-clean code.
"""

import os
import json
from typing import Dict, Optional
from rich.console import Console
from rich.progress import track

from utils.config import config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files, ensure_folder_exists
from ai_engine.hermes.hermes_tagger import tag_file_with_hermes
from ai_engine.cnn.cnn_model import tag_file_with_cnn

console = Console()

def is_tag_valid(tags: Dict[str, str]) -> bool:
    """Checks if tags are valid (non-empty, non-unknown)."""
    for v in tags.values():
        if not v or str(v).lower() in {"", "unknown", "none"}:
            return False
    return True

def analyze_and_tag(audio_path: str, ai_backend: str) -> Optional[Dict[str, str]]:
    """Run AI analysis/tagging and return tags."""
    try:
        if ai_backend == "hermes":
            tags = tag_file_with_hermes(audio_path)
        else:
            tags = tag_file_with_cnn(audio_path)
        if is_tag_valid(tags):
            log_event(f"Analyzed: {audio_path} [{tags}]")
            return tags
        else:
            console.print(f"[yellow]AI returned invalid tags for {audio_path}[/]")
            log_event(f"AI invalid tags for {audio_path}: {tags}")
            return None
    except Exception as e:
        console.print(f"[red]Failed to analyze {audio_path}: {e}[/]")
        log_event(f"Analyze failed for {audio_path}: {e}")
        return None

def batch_ai_analyze_folder(folder: str, ai_backend: str, output_json: bool = True) -> None:
    """
    Batch-analyze all audio files and optionally save results as .json files.
    """
    ensure_folder_exists(folder)
    audio_files = find_all_audio_files(folder, config.SUPPORTED_EXTENSIONS)
    if not audio_files:
        console.print(f"[yellow]No audio files found in {folder}[/]")
        return

    console.print(f"[bold cyan]Analyzing {len(audio_files)} audio files in {folder}...[/]")

    summary = []
    for audio_path in track(audio_files, description="AI-analyzing"):
        tags = analyze_and_tag(audio_path, ai_backend)
        if tags:
            entry = {"path": audio_path, **tags}
            summary.append(entry)
            if output_json:
                json_path = os.path.splitext(audio_path)[0] + ".json"
                with open(json_path, "w") as f:
                    json.dump(tags, f, indent=2)
                console.print(f"[green]Tagged and saved: {audio_path}[/]", highlight=False)
        else:
            summary.append({"path": audio_path, "error": "Tagging failed"})

    # Optional: save a summary file for the batch
    if output_json and summary:
        summary_path = os.path.join(folder, "batch_ai_analysis_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        console.print(f"[bold green]Batch summary saved to: {summary_path}[/bold green]")

def main() -> None:
    """
    CLI entrypoint for batch AI analysis/tagging of all audio files in a folder.
    """
    console.print("[bold magenta]SampleMindAI – Batch AI Analyze[/bold magenta]")
    folder = console.input(f"Enter folder to scan for audio files [{config.SAMPLES_DIR}]: ").strip() or config.SAMPLES_DIR
    if not os.path.isdir(folder):
        console.print(f"[red]Folder '{folder}' does not exist. Aborting.[/]")
        return

    ai_backend = config.AI_BACKEND
    batch_ai_analyze_folder(folder, ai_backend)

    console.print("[bold green]Batch AI analysis process complete![/bold green]")

if __name__ == "__main__":
    main()
