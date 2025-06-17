from utils.config import config
# cli/test_controller.py

from core.control_center.controller import Controller

def main():
    controller = Controller()

    # Test the import_samples module
    controller.import_samples()  # Test import_samples

    # Test the auto_tag_samples module
    controller.auto_tag_samples()  # Test auto_tag_samples

    # Test the export_pack module
    controller.export_pack()  # Test export_pack

    # Test AI analysis
    controller.ai_analysis()  # Test AI analysis

    # Test smart classifier
    controller.smart_classifier()  # Test smart_classifier

    # Test audio repair toolkit
    controller.audio_repair_toolkit()  # Test audio_repair_toolkit

    # Test analyze_audio_stats
    controller.analyze_audio_stats()  # Test analyze_audio_stats

    # Test smart_folder_organizer
    controller.smart_folder_organizer()  # Test smart_folder_organizer

    # Test group_by_folder
    controller.group_by_folder()  # Test group_by_folder

    # Test smart_export
    controller.smart_export()  # Test smart_export

    # Test export_csv
    controller.export_csv()  # Test export_csv

    # Test delete_duplicates
    controller.delete_duplicates()  # Test delete_duplicates

    # Test map_favorites
    controller.map_favorites()  # Test map_favorites

    # Test license_checker
    controller.license_checker()  # Test license_checker

    # Test metadata_bulk_editor
    controller.metadata_bulk_editor()  # Test metadata_bulk_editor

    # Test audio_tools
    controller.audio_tools()  # Test audio_tools

    # Test classify_local_fallback
    controller.classify_local_fallback()  # Test classify_local_fallback

    # Test clean_metadata
    controller.clean_metadata()  # Test clean_metadata

    # Test convert_to_mp3
    controller.convert_to_mp3()  # Test convert_to_mp3

    # Test creative_generator
    controller.creative_generator()  # Test creative_generator

    # Test embedding_search
    controller.embedding_search()  # Test embedding_search

    # Test genre_suggestion
    controller.genre_suggestion()  # Test genre_suggestion

    # Test moodboard_generator
    controller.moodboard_generator()  # Test moodboard_generator

    # Test pack_builder
    controller.pack_builder()  # Test pack_builder

    # Test preprocess
    controller.preprocess()  # Test preprocess

if __name__ == "__main__":
    main()