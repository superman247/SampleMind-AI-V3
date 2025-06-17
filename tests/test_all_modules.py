from utils.config import config
import subprocess

MODULES = [
    "cli/options/auto_tag.py",
    "cli/options/auto_json_tag.py",
    "cli/options/batch_ai_analyze.py",
    "cli/options/smart_classifier.py",
    "cli/options/ai_reanalyze.py",
    "cli/options/assistant_chat.py",
    "cli/options/ai_analysis.py",
    "ai_engine/gpt/auto_json_tag.py",
    "ai_engine/gpt/auto_import_and_tag.py",
    "ai_engine/gpt/gpt_predictor.py",
    "ai_engine/gpt/smart_tag_rater.py",
    "ai_engine/gpt/ai_reanalyzer.py",
    "ai_engine/predictors/smart_classifier.py",
    "ai_engine/gpt/search_tags.py",
    "ai_engine/gpt/tag_analyzer.py",
    "ai_engine/gpt/tag_confidence_visualizer.py",
    "ai_engine/gpt/tag_explorer_ai.py",
    "ai_engine/gpt/tag_explorer_ui.py",
    "ai_engine/gpt/tag_fallback_handler.py",
    "ai_engine/gpt/tag_manager.py",
    "ai_engine/gpt/tag_normalizer.py",
    "ai_engine/gpt/tag_presets.py",
    "ai_engine/gpt/validate_tags.py",
    "ai_engine/gpt/view_tags.py",
    "cli/options/manual_tag.py",
    "cli/options/creative_generator.py",
    "cli/options/analyze_loops.py"
]

def run_module(path):
    print(f"\n--- Testing {path} ---")
    try:
        subprocess.run(["python", path], check=True)
    except Exception as e:
        print(f"Error running {path}: {e}")

for module in MODULES:
    run_module(module)