# cli/menu.py

"""
SampleMindAI – Main CLI Menu
Modern, category-based CLI for accessing all core modules in SampleMindAI.
"""

import sys
import importlib
from typing import Dict, List, Tuple
from rich.console import Console
from rich.prompt import Prompt
from utils.config import config

# Kategorisering av moduler (oppdater ved behov)
CATEGORIES: Dict[str, List[Tuple[str, str]]] = {
    "Import/Tagging": [
        ("Import Samples", "import_samples"),
        ("Auto Tag Samples", "auto_tag"),
        ("Custom Import", "custom_import_samples"),
        ("AI Re-analyze", "ai_reanalyze"),
        ("Auto Import & Tag", "auto_import_and_tag"),
        ("Auto JSON Tag", "auto_json_tag"),
    ],
    "Analyze": [
        ("Analyze Sample", "analyze_sample"),
        ("Analyze Loops", "analyze_loops"),
        ("Analyze Audio Stats", "analyze_audio_stats"),
        ("Analyze Favorites", "analyze_favorites"),
        ("Analyze Recordings", "analyze_recordings"),
    ],
    "Export/Library": [
        ("Export Pack", "export_pack"),
        ("Snapshot Library", "snapshot_library"),
        ("Snapshot Manager", "snapshot_manager"),
        ("Export CSV", "export_csv"),
    ],
    "AI Tools": [
        ("Smart Classifier", "smart_classifier"),
        ("Batch AI Analyze", "batch_ai_analyze"),
        ("Tag Missing Metadata", "tag_missing_metadata"),
        ("Smart Export", "smart_export"),
    ],
    "Batch/Compare": [
        ("Compare Folders", "compare_folders"),
        ("Batch Reanalyze", "batch_reanalyze"),
        ("Classify Local Fallback", "classify_local_fallback"),
    ],
    "Admin & Utils": [
        ("Test All Modules", "test_all_modules"),
        ("Debug Mode", "debug_mode"),
        ("Show Config", "show_config"),
        ("State Sync", "state_sync"),
    ],
    "Audio Tools": [
        ("Audio Repair Toolkit", "audio_repair_toolkit"),
        ("Audio Tools", "audio_tools"),
        ("Convert to MP3", "convert_to_mp3"),
        ("Preprocess", "preprocess"),
        ("Sample Splitter", "sample_splitter"),
        ("Repair Metadata", "repair_metadata"),
    ],
    "Miscellaneous": [
        ("Voice Control", "voice_control"),
        ("Waveform Render CLI", "waveform_render_cli"),
        ("Smart Folder Organizer", "smart_folder_organizer"),
        ("Smart Pack Builder", "smart_pack_builder"),
        ("Map Favorites", "map_favorites"),
        ("Moodboard Generator", "moodboard_generator"),
    ]
}

# Moduler som har CLI entrypoints ligger i cli/options/
OPTIONS_PATH = "cli.options"

console = Console()

def print_menu() -> None:
    console.print("\n[bold cyan]SampleMindAI CLI – Main Menu[/bold cyan]\n")
    for idx, (cat, options) in enumerate(CATEGORIES.items(), 1):
        console.print(f"[bold]{idx}. {cat}[/bold]")
        for opt_idx, (title, _) in enumerate(options, 1):
            console.print(f"    [{idx}.{opt_idx}] {title}")
    console.print("\n[bold]0.[/bold] Exit\n")

def get_menu_map() -> Dict[str, Tuple[str, str]]:
    """
    Map menu index (e.g. '1.2') to (category, module_name)
    """
    menu_map = {}
    for cat_idx, (cat, options) in enumerate(CATEGORIES.items(), 1):
        for opt_idx, (title, module_name) in enumerate(options, 1):
            menu_map[f"{cat_idx}.{opt_idx}"] = (cat, module_name)
    return menu_map

def show_config() -> None:
    """Print current config to terminal."""
    config.print_summary()
    console.input("\nPress Enter to return to the main menu...")

def debug_mode() -> None:
    """Show debug status/info."""
    console.print(f"\n[bold]Debug mode is {'ON' if config.DEBUG_MODE else 'OFF'}[/bold]\n")
    console.input("Press Enter to return to the main menu...")

def run_module(module_name: str) -> None:
    try:
        mod = importlib.import_module(f"{OPTIONS_PATH}.{module_name}")
        if hasattr(mod, "main"):
            mod.main()
        else:
            console.print(f"[red]Module '{module_name}' does not have a main() function![/red]")
    except Exception as e:
        console.print(f"[red]Error running module '{module_name}': {e}[/red]")
        if config.DEBUG_MODE:
            import traceback
            traceback.print_exc()
    input("\nPress Enter to return to the menu...")

def main() -> None:
    while True:
        print_menu()
        menu_map = get_menu_map()
        choice = Prompt.ask("\nSelect option", default="0")
        if choice == "0":
            console.print("\nExiting SampleMindAI. Goodbye!\n")
            sys.exit(0)
        elif choice in menu_map:
            cat, module_name = menu_map[choice]
            if module_name == "show_config":
                show_config()
            elif module_name == "debug_mode":
                debug_mode()
            else:
                run_module(module_name)
        else:
            console.print("[red]Invalid choice. Try again![/red]\n")

if __name__ == "__main__":
    main()
