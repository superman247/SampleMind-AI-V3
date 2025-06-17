from utils.config import config
# core/control_center/controller.py
import logging
import importlib
from typing import Callable

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# core/control_center/controller.py
class Controller:
    def __init__(self):
        # Module registry can be dynamically populated
        self.modules = {
            "import_samples": "cli.options.import_samples",
            "auto_tag_samples": "cli.options.auto_tag",
            "manual_tag_samples": "cli.options.manual_tag",
            "export_pack": "cli.options.export_pack",
            "bookmark_export": "cli.options.bookmark_export",
            "ai_analysis": "cli.options.ai_analysis",
            "smart_classifier": "cli.options.smart_classifier",
            "audio_repair_toolkit": "cli.options.audio_repair_toolkit",
            "analyze_audio_stats": "cli.options.analyze_audio_stats",
            "smart_folder_organizer": "cli.options.smart_folder_organizer",
            "group_by_folder": "cli.options.group_by_folder",
            "smart_export": "cli.options.smart_export",
            "export_csv": "cli.options.export_csv",
            "delete_duplicates": "cli.options.delete_duplicates",
            "map_favorites": "cli.options.map_favorites",
            "license_checker": "cli.options.license_checker",
            "metadata_bulk_editor": "cli.options.metadata_bulk_editor",
            "audio_tools": "cli.options.audio_tools",
            "classify_local_fallback": "cli.options.classify_local_fallback",
            "clean_metadata": "cli.options.clean_metadata",
            "convert_to_mp3": "cli.options.convert_to_mp3",
            "creative_generator": "cli.options.creative_generator",
            "embedding_search": "cli.options.embedding_search",
            "genre_suggestion": "cli.options.genre_suggestion",
            "moodboard_generator": "cli.options.moodboard_generator",
            "pack_builder": "cli.options.pack_builder",
            "preprocess": "cli.options.preprocess"
        }


    

    def execute_module_by_name(self, module_name: str) -> None:
        """
        Dynamically import and run a CLI module.
        Assumes each module has a `main()` function.
        
        Args:
            module_name (str): Name of the module to execute.
        """
        module_path = self.modules.get(module_name)
        if not module_path:
            logger.error(f"Module {module_name} not found in registry.")
            return

        try:
            logger.info(f"Attempting to execute module: {module_name}")
            module = importlib.import_module(module_path)

            if not hasattr(module, 'main'):
                raise AttributeError(f"Module {module_name} does not contain a 'main' function.")

            logger.info(f"Executing {module_name} main function.")
            module.main()

        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {str(e)}")
        except AttributeError as e:
            logger.error(f"Error in module {module_name}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in module {module_name}: {str(e)}")

    def import_samples(self):
        print("Importing samples...")
        self.execute_module_by_name("import_samples")

    def auto_tag_samples(self):
        print("Auto-tagging samples...")
        self.execute_module_by_name("auto_tag_samples")

    def manual_tag_samples(self):
        print("Manual tagging samples...")
        self.execute_module_by_name("manual_tag_samples")

    def export_pack(self):
        print("Exporting pack...")
        self.execute_module_by_name("export_pack")

    def bookmark_export(self):
        print("Exporting bookmarks...")
        self.execute_module_by_name("bookmark_export")

    def ai_analysis(self):
        print("Running AI analysis...")
        self.execute_module_by_name("ai_analysis")

    def smart_classifier(self):
        print("Running smart classifier...")
        self.execute_module_by_name("smart_classifier")

    def audio_repair_toolkit(self):
        print("Audio repair toolkit selected...")
        self.execute_module_by_name("audio_repair_toolkit")

    def analyze_audio_stats(self):
        print("Analyzing audio stats...")
        self.execute_module_by_name("analyze_audio_stats")

    def smart_folder_organizer(self):
        print("Organizing samples into folders...")
        self.execute_module_by_name("smart_folder_organizer")

    def group_by_folder(self):
        print("Grouping samples by folder...")
        self.execute_module_by_name("group_by_folder")

    def smart_export(self):
        print("Smart exporting...")
        self.execute_module_by_name("smart_export")

    def export_csv(self):
        print("Exporting CSV...")
        self.execute_module_by_name("export_csv")

    def delete_duplicates(self):
        print("Deleting duplicate samples...")
        self.execute_module_by_name("delete_duplicates")

    def map_favorites(self):
        print("Mapping favorite samples...")
        self.execute_module_by_name("map_favorites")

    def license_checker(self):
        print("Checking licenses for samples...")
        self.execute_module_by_name("license_checker")

    def metadata_bulk_editor(self):
        print("Editing metadata for samples...")
        self.execute_module_by_name("metadata_bulk_editor")

    def audio_tools(self):
        print("Running audio tools...")
        self.execute_module_by_name("audio_tools")

    def classify_local_fallback(self):
        print("Running local fallback classifier...")
        self.execute_module_by_name("classify_local_fallback")

    def clean_metadata(self):
        print("Cleaning metadata for samples...")
        self.execute_module_by_name("clean_metadata")

    def convert_to_mp3(self):
        print("Converting samples to MP3...")
        self.execute_module_by_name("convert_to_mp3")

    def creative_generator(self):
        print("Generating creative variations...")
        self.execute_module_by_name("creative_generator")

    def embedding_search(self):
        print("Searching for similar samples...")
        self.execute_module_by_name("embedding_search")

    def genre_suggestion(self):
        print("Suggesting genre based on audio features...")
        self.execute_module_by_name("genre_suggestion")

    def moodboard_generator(self):
        print("Generating moodboard...")
        self.execute_module_by_name("moodboard_generator")

    def pack_builder(self):
        print("Building a sample pack...")
        self.execute_module_by_name("pack_builder")

    def preprocess(self):
        print("Preprocessing audio samples...")
        self.execute_module_by_name("preprocess")