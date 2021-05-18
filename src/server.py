from flask import \
    Flask, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    session, \
    flash
from .config import \
    SAVED_REPLAY_FOLDER, \
    USER_UPLOAD_FOLDER
from .constants import \
    SC2REPLAY, \
    OWN_REPLAY_TAG, \
    BENCH_REPLAY_TAG, \
    SAVED_REPLAYS_TAG, \
    INDEX_HTML, \
    ANALYZE_HTML, \
    FLASK_CONFIG, \
    SESSION_FILENAME_DATA

from .utils import valid_names, get_file_hash
from . import replayparser
from zephyrus_sc2_parser.exceptions import PlayerCountError
import os

app = Flask(__name__)

FILE_DIR = os.path.dirname(__file__)

saved_replay_folder_path = os.path.join(
    FILE_DIR,
    SAVED_REPLAY_FOLDER)

user_upload_folder_path = os.path.join(
    FILE_DIR,
    USER_UPLOAD_FOLDER)


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

    if not valid_names(request):
        flash("Error in request name variables")
        return redirect(request.url)

    # type werkzeug.FileStorage
    own_replay_file = request.files[OWN_REPLAY_TAG]
    bench_replay_file = request.files[BENCH_REPLAY_TAG]
    own_replay_filename = own_replay_file.filename
    bench_replay_filename = bench_replay_file.filename

    # checks whether a file was uploaded
    if own_replay_filename == '':
        flash("You must supply your own replay!")
        return redirect(request.url)
    elif bench_replay_filename == '' and not request.form:
        flash("You must have a benchmark replay!")
        return redirect(request.url)
    elif bench_replay_filename != '' and request.form:
        flash("You cannot have two benchmarks selected!")
        return redirect(request.url)

    # All cases below should be allowed
    # saves own_replay temp copy
    own_replay = own_replay_file.read()
    own_replay_hash = get_file_hash(own_replay)
    own_replay_filename = os.path.join(
        user_upload_folder_path,
        own_replay_hash + '.' + SC2REPLAY)
    own_replay_file.close()
    with open(own_replay_filename, 'wb') as f:
        f.write(own_replay)

    # if request.form uses SAVED_REPLAYS_TAG, we use saved replays
    if request.form:
        savedfileName = request.form.get(SAVED_REPLAYS_TAG) \
            + "." \
            + SC2REPLAY

        bench_replay_filename = os.path.join(
            saved_replay_folder_path,
            savedfileName)
    # otherwise, use uploaded benchmark replay
    else:
        # saves temp copy of benchmark replay
        bench_replay = bench_replay_file.read()
        bench_replay_hash = get_file_hash(bench_replay)
        bench_replay_filename = os.path.join(
            user_upload_folder_path,
            bench_replay_hash + '.' + SC2REPLAY)
        bench_replay_file.close()
        with open(bench_replay_filename, 'wb') as f:
            f.write(bench_replay)

    analyze_url = url_for(
        'analyze',
        hash=own_replay_hash)

    session[SESSION_FILENAME_DATA] = {
        'filename_own': own_replay_filename,
        'filename_bench': bench_replay_filename
    }

    return redirect(analyze_url)


@app.route('/<hash>', methods=['GET'])
def analyze(hash: str):
    """analyzes the replay with the given filehash.
    And returns the html page that displays the graphs.

    Parameters:
    - hash: the hash of user-uploaded file
        (uploaded file should have been renamed to its hash)
    """
    # TODO
    filenames = session.get(SESSION_FILENAME_DATA, None)
    filename_bench = None
    filename_own = None

    if filenames is not None:
        filename_bench = filenames['filename_bench']
        filename_own = filenames['filename_own']
    else:
        flash("Session Expired")
        return redirect(url_for('index'))

    # validates the replay files as an actual replay that can be parsed.
    bench_replay = None
    own_replay = None
    try:
        bench_replay = replayparser.load_replay_file(
            filename_bench)
        own_replay = replayparser.load_replay_file(
            filename_own)
    except PlayerCountError:
        flash("Only two player replays are supported!")
        return redirect(url_for('index'))
    except Exception:
        flash("Unable to read replay")
        return redirect(url_for('index'))

    bench_player_names, own_player_names = replayparser.dual_data(
        replayparser.get_player_names,
        bench_replay, own_replay
    )
    bench_timestamps, own_timestamps = replayparser.dual_data(
        replayparser.get_timeline_data,
        bench_replay, own_replay
    )
    bench_minerals, own_minerals = replayparser.dual_data(
        replayparser.get_mineral_data,
        bench_replay, own_replay
    )
    bench_gas, own_gas = replayparser.dual_data(
        replayparser.get_gas_data,
        bench_replay, own_replay
    )
    bench_workers_produce, own_workers_produce = replayparser.dual_data(
        replayparser.get_workers_produced,
        bench_replay, own_replay
    )

    return render_template(
        ANALYZE_HTML,
        bench_players=bench_player_names, own_players=own_player_names,
        bench_timestamps=bench_timestamps, own_timestamps=own_timestamps,
        bench_minerals=bench_minerals, own_minerals=own_minerals,
        bench_gas=bench_gas, own_gas=own_gas,
        bench_workers_produce=bench_workers_produce, own_workers_produce=own_workers_produce)


def run_server():
    """Configures, then runs the Flask server."""
    app.config.from_pyfile(FLASK_CONFIG)

    # creates the user upload and saved replays folders
    if not os.path.isdir(user_upload_folder_path):
        os.mkdir(user_upload_folder_path)
    if not os.path.isdir(saved_replay_folder_path):
        os.mkdir(saved_replay_folder_path)

    # starts the server
    app.run()
