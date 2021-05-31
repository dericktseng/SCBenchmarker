import os

"""=== Program configurations === """

""" directory of the root of the project """
PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

""" path to the folder containing saved benchmark replays """
SAVED_REPLAY_FOLDER_PATH = os.path.join(PROJ_DIR, 'saved-replays')

""" path to the folder containing replays the user uploads """
USER_UPLOAD_FOLDER_PATH = os.path.join(PROJ_DIR, 'user-replays')

"""time between measuring a data point"""
DELTA_SECOND = 2

""" Allows multiprocess loading of replays. """
MULTIPROCESS = True

""" Number of workers for multiprocessing. None defaults to 61.
Documentation here: https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor"""
MAX_WORKERS = 2


"""=== Flask configuration ==="""

SECRET_KEY = os.urandom(24)
FLASK_ENV = 'development'  # development or production
DEBUG = True
TESTING = True
UPLOAD_FOLDER = USER_UPLOAD_FOLDER_PATH
SERVER_NAME = '127.0.0.1:9999'

