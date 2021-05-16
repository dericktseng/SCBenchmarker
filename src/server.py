from flask import Flask
from flask import render_template

app = Flask(__name__)
FLASK_CONFIG = 'config.py'


@app.route('/')
def index():
    """Renders the index file to be served at root."""
    return render_template('index.html')


@app.route('/<filehash>')
def analyze(filehash: str):
    """analyzes the replay with the given filehash.
    And returns the html page that displays the graphs.

    Parameters:
    - filehash: the hash of the uploaded file
        (uploaded file should have been renamed to its hash)
    """
    # TODO
    return filehash


def run_server():
    """Configures, then runs the Flask server."""
    app.config.from_pyfile(FLASK_CONFIG)
    app.run()
