from utils.config import config
# core/bootstrap.py
import os
import logging

# Setup logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_application():
    """
    Initializes the application by loading configuration settings and setting up necessary directories.
    """
    try:
        # Example initialization task (ensure directories exist)
        required_dirs = ["data/samples", "data/loops", "data/recordings"]
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(f"Created missing directory: {dir_path}")

        logger.info("Application initialized successfully.")

    except Exception as e:
        logger.error(f"Error during application initialization: {str(e)}")

if __name__ == "__main__":
    initialize_application()