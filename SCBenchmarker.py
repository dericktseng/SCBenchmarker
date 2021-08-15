from src.server import app as application
from src.constants import FLASK_CONFIG
from src.config import PROJ_DIR, TESTING
from shutil import copy2
import os

if __name__ == "__main__":
    # checks whether env file exists
    envfilepath = os.path.join(PROJ_DIR, '.env')
    tmpenvfilepath = os.path.join(PROJ_DIR, 'template.env')
    if not os.path.isfile(envfilepath):
        print(".env file does not exist")
        print("please modify the env file!")
        copy2(tmpenvfilepath, envfilepath)
        exit(1)

    # Configures, then runs the Flask server.
    application.config.from_pyfile(FLASK_CONFIG)

    if TESTING:
        for key in application.config:
            print(key, application.config[key])

    # starts the server
    application.run()
