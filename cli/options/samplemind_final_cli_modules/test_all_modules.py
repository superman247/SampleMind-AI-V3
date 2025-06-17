# cli/options/test_all_modules.py
"""
Runs tests on all CLI modules in the SampleMindAI project to verify functionality.
Uses logging, config, and proper error handling. Automatically detects and runs modules.
"""

import importlib
import os
import traceback
from pathlib import Path
from typing import List

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

from utils.config import get_config
from utils.logger import log_event

console = Console()
config = get_config()
MODULES_DIR = Path("cli/options")

EXCLUDE_FILES = [
    "__init__.py",
    "menu.py",
    "test_all_modules.py",
    "waveform_render_cli.py",  # May require audio rendering engine
    "library.py",              # Still in-progress
]

def find_modules_to_test() -> List[str]:
    modules = []
    for file in MODULES_DIR.glob("*.py"):
        if file.name in EXCLUDE_FILES:
            continue
        modules.append(file.stem)
    return sorted(modules)

def run_module(module_name: str) -> bool:
    try:
        console.print(f"[bold cyan]Running:[/bold cyan] {module_name}")
        module = importlib.import_module(f"cli.options.{module_name}")
        if hasattr(module, "main"):
            module.main(debug=True)
            log_event("test_module_success", {"module": module_name})
            return True
        else:
            raise AttributeError("No 'main(debug=True)' function found")
    except Exception as e:
        log_event("test_module_failure", {"module": module_name, "error": str(e)})
        traceback.print_exc()
        return False

def main():
    console.rule("[bold green]SampleMindAI – CLI Batch Tester")
    modules = find_modules_to_test()
    results = {}

    for name in modules:
        success = run_module(name)
        results[name] = "✅" if success else "❌"

    # Display summary
    table = Table(title="Test Results")
    table.add_column("Module", style="bold white")
    table.add_column("Status", style="bold green")
    for mod, res in results.items():
        table.add_row(mod, res)
    console.print(table)

    failures = [m for m, r in results.items() if r == "❌"]
    if failures:
        console.print(f"[bold red]Failed Modules:[/bold red] {', '.join(failures)}")
    else:
        console.print("[bold green]All modules ran successfully![/bold green]")

    Confirm.ask("[bold yellow]Return to menu?[/bold yellow]", default=True)

if __name__ == "__main__":
    main()
