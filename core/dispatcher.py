from utils.config import config
# core/dispatcher.py
from core.control_center.controller import Controller

# Create an instance of the Controller
controller = Controller()

def dispatch_module(module_name: str):
    """
    Dispatch the module by its name, using the controller to execute it.
    Args:
        module_name (str): Name of the module to execute.
    """
    try:
        print(f"Attempting to dispatch module: {module_name}...")
        # Dynamically dispatch module using the Controller instance
        controller.execute_module_by_name(module_name)

    except Exception as e:
        # Catch any errors and log them
        print(f"Error while dispatching module {module_name}: {str(e)}")
        logger.error(f"Error while dispatching module {module_name}: {str(e)}")

# Example usage: Dispatch a module based on its name (replace with actual module name)
# dispatch_module("auto_tag.py")