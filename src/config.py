import os
from dotenv import load_dotenv

load_dotenv()

""" directory of the root of the project """
PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

""" path to the folder containing saved benchmark replays """
SAVED_REPLAY_FOLDER_PATH = os.getenv('SAVED_FOLDER_PATH') or os.path.join(PROJ_DIR, 'saved-replays')

""" path to the folder containing replays the user uploads """
USER_UPLOAD_FOLDER_PATH = os.getenv('UPLOAD_FOLDER_PATH') or os.path.join(PROJ_DIR, 'user-replays')

""" Allows multiprocess loading of replays. """
MULTIPROCESS = bool(os.getenv("MULTIPROCESS"))

""" Number of workers for multiprocessing. None defaults to 61.
Documentation here: https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor"""
MAX_WORKERS = os.getenv('MAX_WORKERS')
MAX_WORKERS = int(MAX_WORKERS) if MAX_WORKERS else 2

"""=== Flask configuration ==="""
FLASK_ENV = os.getenv('FLASK_ENV')
DEBUG = bool(os.getenv('DEBUG'))
TESTING = bool(os.getenv('TESTING'))
SERVER_NAME = os.getenv('SERVER_NAME')
