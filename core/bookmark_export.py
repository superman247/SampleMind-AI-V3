from utils.config import config
# cli/options/bookmark_export.py
import os
import json

def export_bookmarks(bookmarked_samples):
    """
    Export the bookmarked samples to a JSON file.
    """
    export_path = "data/bookmarks.json"  # Path to save the exported bookmarks

    try:
        with open(export_path, "w") as bookmark_file:
            json.dump(bookmarked_samples, bookmark_file)
        print(f"Bookmarks successfully exported to {export_path}.")
    except Exception as e:
        print(f"Error exporting bookmarks: {e}")

def main():
    """
    Main function for exporting bookmarks.
    """
    bookmarked_samples = ["sample1.wav", "sample2.wav"]  # Placeholder for actual bookmarks
    export_bookmarks(bookmarked_samples)

if __name__ == "__main__":
    main()