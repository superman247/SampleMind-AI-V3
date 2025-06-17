from utils.config import config
# core/control_center/menu.py
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table  # Import Table from rich.table
from core.control_center.controller import Controller

# Initialize console for output
console = Console()

# Instantiate controller
controller = Controller()

# Main Menu Function
def main_menu():
    print("Starting SampleMind Menu...")  # Debugging line to check if the function starts
    while True:
        table = Table(title="SampleMind CLI - Main Menu", show_header=True, header_style="bold magenta")
        table.add_column("Choice", justify="center")
        table.add_column("Description", justify="center")

        # Add categories and options to the menu
        table.add_row("[1] Import Options", "Manage import and training data operations.")
        table.add_row("[2] Tagging Options", "Auto-tag and manage sample metadata.")
        table.add_row("[3] Export Options", "Export your samples or packs.")
        table.add_row("[4] AI Tools", "AI analysis, prediction, and tagging tools.")
        table.add_row("[5] Audio Tools", "Various tools for audio analysis and repair.")
        table.add_row("[6] Sample Organization", "Organize and group your samples effectively.")
        table.add_row("[7] Export Settings", "Advanced exporting and smart pack building.")
        table.add_row("[8] Exit", "Exit the program.")

        console.print(table)
        choice = Prompt.ask("Please choose an option", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="8")

        # Execute corresponding function for the selected choice
        if choice == "1":
            import_options()
        elif choice == "2":
            tagging_options()
        elif choice == "3":
            export_options()
        elif choice == "4":
            ai_tools()
        elif choice == "5":
            audio_tools()
        elif choice == "6":
            sample_organization()
        elif choice == "7":
            export_settings()
        elif choice == "8":
            console.print("Exiting... Goodbye!", style="bold red")
            break  # This will exit the loop and end the program

def import_options():
    print("Importing options selected...")  # Debugging line to confirm method is called
    controller.import_samples()  # Ensure this method is implemented in controller

def tagging_options():
    print("Tagging options selected...")  # Debugging line to confirm method is called
    controller.auto_tag_samples()  # Ensure this method is implemented in controller
    controller.manual_tag_samples()  # Ensure this method is implemented in controller

def export_options():
    print("Export options selected...")  # Debugging line to confirm method is called
    controller.export_pack()  # Ensure this method is implemented in controller
    controller.bookmark_export()  # Ensure this method is implemented in controller

def ai_tools():
    print("AI Tools selected...")  # Debugging line to confirm method is called
    controller.ai_analysis()  # Ensure this method is implemented in controller
    controller.smart_classifier()  # Ensure this method is implemented in controller

def audio_tools():
    print("Audio Tools selected...")  # Debugging line to confirm method is called
    controller.audio_repair_toolkit()  # Ensure this method is implemented in controller
    controller.analyze_audio_stats()  # Ensure this method is implemented in controller

def sample_organization():
    print("Sample Organization selected...")  # Debugging line to confirm method is called
    controller.smart_folder_organizer()  # Ensure this method is implemented in controller
    controller.group_by_folder()  # Ensure this method is implemented in controller

def export_settings():
    print("Export Settings selected...")  # Debugging line to confirm method is called
    controller.smart_export()  # Ensure this method is implemented in controller
    controller.export_csv()  # Ensure this method is implemented in controller

# Add this to start the menu when running the script
if __name__ == "__main__":
    main_menu()  # This will start the menu