import os
import re
import shutil

# List all the replacements you want
REPLACEMENTS = {
    "config.SAMPLES_DIR": "config.SAMPLES_DIR",
    "config.LOOPS_DIR": "config.LOOPS_DIR",
    "config.AUDIO_DIR": "config.AUDIO_DIR",
    "config.AI_BACKEND": "config.AI_BACKEND",
    "config.HERMES_MODEL": "config.HERMES_MODEL",
    "config.CACHE_DIR": "config.CACHE_DIR",
    "config.SUPPORTED_EXTENSIONS": "config.config.SUPPORTED_EXTENSIONS",
    "config.OPENAI_API_KEY": "config.OPENAI_API_KEY"
}

IMPORT_PATTERN = re.compile(r"from\s+utils\.config\s+import\s+.+")
CONFIG_IMPORT = "from utils.config import config"

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    # Remove old import lines and ensure config-import is present at top
    lines = code.splitlines()
    new_lines = []
    config_imported = False
    for line in lines:
        if IMPORT_PATTERN.match(line):
            continue
        if CONFIG_IMPORT in line:
            config_imported = True
        new_lines.append(line)
    code = "\n".join(new_lines)
    if not config_imported:
        code = CONFIG_IMPORT + "\n" + code

    # Replace all old constants with config usage
    for old, new in REPLACEMENTS.items():
        code = re.sub(rf"\b{old}\b", new, code)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

def backup_and_process(directory, extensions=(".py",)):
    backup_dir = directory + "_bak_configfix"
    if not os.path.exists(backup_dir):
        shutil.copytree(directory, backup_dir)
        print(f"[INFO] Backup created: {backup_dir}")
    for root, _, files in os.walk(directory):
        for fname in files:
            if fname.endswith(extensions):
                fpath = os.path.join(root, fname)
                process_file(fpath)
                print(f"[FIXED] {fpath}")

if __name__ == "__main__":
    # Set to your project root folder (where cli/, ai_engine/, utils/ ligger)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    backup_and_process(PROJECT_ROOT)
    print("[DONE] All .py files have been converted to use config-object.")