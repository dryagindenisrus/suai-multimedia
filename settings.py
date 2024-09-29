from pathlib import Path

# Base directory of the project (the root folder where settings.py is located)
BASE_DIR = Path(__file__).resolve().parent

# Directory where resources (e.g., video, audio files) are stored
RESOURCES_DIR = BASE_DIR / "resources"

# Directory for result
RESULT_DIR = BASE_DIR / "result"

# Supported file formats for video
VIDEO_FORMATS = ['avi']

# Configuration settings for video and audio processing
MAX_VIDEO_RESOLUTION = (1920, 1080)  # Maximum video resolution (width, height)
MAX_AUDIO_CHANNELS = 2  # Maximum number of audio channels

# Toggle debug mode (True for development, False for production)
DEBUG = True
