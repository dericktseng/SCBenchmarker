"""=== Other configurations ==="""
"""All Folder paths are relative to THIS FILE config.py
Either relative or absolute paths are accepted."""

"""The folder that stores the professional benchmarks.
All files in here CANNOT be deleted."""
SAVED_REPLAY_FOLDER = '../test-replays'

"""The folder that stores the user replays.
All files in here CAN be deleted."""
USER_UPLOAD_FOLDER = '../user-replays'

"""time between measuring a data point"""
DELTA_SECOND = 5


"""=== Flask configuration ==="""
FLASK_ENV = 'development'
DEBUG = True
TESTING = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = USER_UPLOAD_FOLDER
