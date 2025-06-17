# cli/options/waveform_render_cli.py
"""
Waveform Renderer (CLI) – Renders waveform images for audio files.
Used by GUI preview, export snapshots, and moodboard.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import librosa
import librosa.display

from rich.console import Console
from rich.prompt import Prompt
from utils.config import get_config
from utils.logger import log_event
from utils.file_utils import find_all_audio_files

console = Console()
config = get_config()


def render_waveform(file_path: Path, output_folder: Path) -> Path:
    try:
        y, sr = librosa.load(file_path, sr=None)
        plt.figure(figsize=(10, 3))
        librosa.display.waveshow(y, sr=sr, alpha=0.8)
        plt.axis("off")

        output_folder.mkdir(parents=True, exist_ok=True)
        out_path = output_folder / (file_path.stem + "_waveform.png")
        plt.savefig(out_path, bbox_inches="tight", pad_inches=0)
        plt.close()
        return out_path
    except Exception as e:
        console.print(f"[red]Failed to render waveform: {e}")
        log_event("waveform_render_failed", {"file": str(file_path), "error": str(e)})
        return None

def main(debug: bool = False):
    console.rule("[bold blue]SampleMindAI – Waveform Renderer")
    folder = Prompt.ask("Enter folder path", default=config["sample_library"])
    output = Prompt.ask("Enter output folder", default="data/waveforms")

    folder_path = Path(folder).expanduser()
    output_path = Path(output).expanduser()

    if not folder_path.exists():
        console.print("[bold red]Input folder does not exist.")
        return

    audio_files = find_all_audio_files(folder_path)
    if not audio_files:
        console.print("[yellow]No audio files found in the folder.")
        return

    for path in audio_files:
        console.print(f"[cyan]Rendering:[/cyan] {path.name}")
        image_path = render_waveform(path, output_path)
        if image_path:
            console.print(f"[green]Saved:[/green] {image_path}")
            log_event("waveform_rendered", {"file": str(path), "output": str(image_path)})

if __name__ == "__main__":
    main()
