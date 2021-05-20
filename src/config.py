import os

"""=== Program configurations ==="""

"""All Folder paths are relative to THIS FILE (config.py).
TODO - allow absolute paths as well"""

"""The folder that stores the professional benchmarks."""
SAVED_REPLAY_FOLDER = '../test-replays'

"""The folder that stores the user replays."""
USER_UPLOAD_FOLDER = '../user-replays'

"""time between measuring a data point"""
DELTA_SECOND = 3


"""=== Flask configuration ==="""

SECRET_KEY = os.urandom(24)
FLASK_ENV = 'development'  # development or production
DEBUG = True
TESTING = True
UPLOAD_FOLDER = USER_UPLOAD_FOLDER
SERVER_NAME = '127.0.0.1:9999'
