from src.server import app as application
from src.constants import FLASK_CONFIG
from src.config import USER_UPLOAD_FOLDER_PATH, SAVED_REPLAY_FOLDER_PATH
import os

if __name__ == "__main__":
    """Configures, then runs the Flask server."""
    application.config.from_pyfile(FLASK_CONFIG)

    # creates the user upload and saved replays folders
    if not os.path.isdir(USER_UPLOAD_FOLDER_PATH):
        os.mkdir(USER_UPLOAD_FOLDER_PATH)
    if not os.path.isdir(SAVED_REPLAY_FOLDER_PATH):
        os.mkdir(SAVED_REPLAY_FOLDER_PATH)

    # starts the server
    application.run()
