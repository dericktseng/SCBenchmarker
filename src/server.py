from flask import Flask, flash, render_template, request, redirect, url_for
from .config import SAVED_REPLAY_FOLDER
from .constants import SC2REPLAY
from .constants import OWN_REPLAY_TAG
from .constants import BENCH_REPLAY_TAG
from .constants import SAVED_REPLAYS_TAG
from .constants import INDEX_HTML
from .constants import FLASK_CONFIG
import os
import hashlib

app = Flask(__name__)


FILE_DIR = os.path.dirname(__file__)
saved_replay_folder_path = os.path.join(
        FILE_DIR,
        SAVED_REPLAY_FOLDER)
hashFunc = hashlib.md5()


def get_file_hash(filedata):
    return hashlib.md5(filedata).hexdigest()


@app.route('/', methods=['GET'])
def index():
    """Renders the index file to be served at root."""

    replays = os.listdir(saved_replay_folder_path)

    # strips .SC2Replay extension from replay name
    extlength = len('.{}'.format(SC2REPLAY))
    replays = [replay[:-extlength] for replay in replays]

    return render_template(
        INDEX_HTML,
        saved_replays=replays,
        saved_replay_tag=SAVED_REPLAYS_TAG,
        own_replay_tag=OWN_REPLAY_TAG,
        bench_replay_tag=BENCH_REPLAY_TAG)


@app.route('/', methods=['POST'])
def upload_replays():
    """Reads the replays to be analyzed."""

    # checks whether incoming data has correct names
    if OWN_REPLAY_TAG not in request.files:
        flash('OWN_REPLAY not found in request')
        return redirect(request.url)
    elif BENCH_REPLAY_TAG not in request.files:
        flash('BENCH_REPLAY not found in request')
        return redirect(request.url)

    # type werkzeug.FileStorage
    own_replay_file = request.files[OWN_REPLAY_TAG]
    bench_replay_file = request.files[BENCH_REPLAY_TAG]

    # checks whether a file was uploaded
    if own_replay_file.filename == '':
        flash("You must supply your own replay!")
        return redirect(request.url)
    elif bench_replay_file.filename == '' and not request.form:
        flash("You must have a benchmark replay!")
        return redirect(request.url)
    elif bench_replay_file.filename != '' and request.form:
        flash("You cannot have two benchmarks selected!")
        return redirect(request.url)
    # if request asks for a saved replay, store to bench_replay_file.
    elif bench_replay_file.filename == '' and request.form:
        savedfileName = request.form.get(SAVED_REPLAYS_TAG) \
            + "." \
            + SC2REPLAY

        saved_replay_path = os.path.join(
            saved_replay_folder_path,
            savedfileName)
        bench_replay_file = open(saved_replay_path, 'rb')

    own_replay = own_replay_file.read()
    bench_replay = bench_replay_file.read()
    user_hash = get_file_hash(own_replay)
    bench_hash = get_file_hash(bench_replay)

    own_replay_file.close()
    bench_replay_file.close()

    analyze_url = url_for(
        'analyze',
        filehashbench=bench_hash,
        filehashuser=user_hash)

    return redirect(analyze_url)


@app.route('/<filehashbench>/<filehashuser>')
def analyze(filehashbench: str, filehashuser: str):
    """analyzes the replay with the given filehash.
    And returns the html page that displays the graphs.

    Parameters:
    - filehash: the hash of the uploaded file
        (uploaded file should have been renamed to its hash)
    """
    # TODO
    return str(filehashbench) + " " + filehashuser


def run_server():
    """Configures, then runs the Flask server."""
    app.config.from_pyfile(FLASK_CONFIG)
    app.run()
