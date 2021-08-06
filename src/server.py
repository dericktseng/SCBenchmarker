import os
from flask import \
    Flask, \
    render_template, \
    request, \
    redirect, \
    url_for

from .config import \
    MULTIPROCESS, \
    MAX_WORKERS, \
    SAVED_REPLAY_FOLDER_PATH, \
    USER_UPLOAD_FOLDER_PATH

from .constants import \
    SC2REPLAY, \
    OWN_REPLAY_TAG, \
    BENCH_REPLAY_TAG, \
    SAVED_REPLAYS_TAG, \
    INDEX_HTML, \
    ANALYZE_HTML

from . import utils
from .replayparser import ReplayData

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """ Renders the index file to be served. """

    replays = os.listdir(SAVED_REPLAY_FOLDER_PATH)
    errors = request.args.get('error', default=None, type=str)

    # strips .SC2Replay extension from replay name
    extlength = len('.{}'.format(SC2REPLAY))
    replays = [replay[:-extlength] for replay in replays].sort()

    return render_template(
        INDEX_HTML,
        errors=errors,
        saved_replays=replays,
        saved_replay_tag=SAVED_REPLAYS_TAG,
        own_replay_tag=OWN_REPLAY_TAG,
        bench_replay_tag=BENCH_REPLAY_TAG)


@app.route('/', methods=['POST'])
def upload_replays():
    """ Reads the replays to be analyzed. """

    if not utils.valid_names(request):
        errormsg = 'Error in request name variables'
        return redirect(url_for('index', error=errormsg))

    # type werkzeug.FileStorage, this is the files and names
    # that the user uploads, not the hashed versions.
    own_replay_file = request.files[OWN_REPLAY_TAG]
    bench_replay_file = request.files[BENCH_REPLAY_TAG]
    own_replay_filename = own_replay_file.filename
    bench_replay_filename = bench_replay_file.filename

    # checks whether a file was uploaded
    if own_replay_filename == '':
        errormsg = 'You must supply your own replay!'
        return redirect(url_for('index', error=errormsg))
    elif bench_replay_filename == '' and not request.form:
        errormsg = 'You must have a benchmark replay!'
        return redirect(url_for('index', error=errormsg))
    elif bench_replay_filename != '' and request.form:
        errormsg = 'You cannot have two benchmarks selected!'
        return redirect(url_for('index', error=errormsg))

    # All cases below should be allowed
    own_replay_filename = utils.write_replay_file(own_replay_file)

    # name of benchmark replay filename (to pass to analyze)
    bench_replay_filename = ''

    # if request.form uses SAVED_REPLAYS_TAG, we use saved replays
    # otherwise, use uploaded benchmark replay
    use_saved_replay = False

    if request.form:
        use_saved_replay = True
        savedfileName = request.form.get(SAVED_REPLAYS_TAG)
        if not savedfileName:
            errormsg = "Form unable to be completed. No element SAVED_REPLAYS_TAG"
            return redirect(url_for('index', error=errormsg))
        bench_replay_filename = os.path.join(
            SAVED_REPLAY_FOLDER_PATH,
            savedfileName + '.' + SC2REPLAY)
    else:
        bench_replay_filename = utils.write_replay_file(bench_replay_file)

    analyze_url = url_for(
        'analyze',
        basename_bench=os.path.basename(bench_replay_filename),
        basename_own=os.path.basename(own_replay_filename),
        use_saved_replay=use_saved_replay)

    return redirect(analyze_url)


@app.route('/analyze', methods=['GET'])
def analyze():
    """analyzes the replay with the given filehash.
    And returns the html page that displays the graphs.

    Parameters:
    - basename_bench - basename of the benchmark replay
    - basename_own - basename of user-uploaded own replay
    - use_saved_replay - whether the benchmark is a saved replay
    """
    filename_bench = request.args.get('basename_bench', default=None, type=str)
    filename_own = request.args.get('basename_own', default=None, type=str)

    # although this is passed in as a boolean, it gets converted to a string.
    use_saved_replay = request.args.get('use_saved_replay', default=None)

    if filename_bench is None or filename_own is None or use_saved_replay is None:
        errormsg = 'Replay files cannot be found (Did you upload a replay?)'
        return redirect(url_for('index', error=errormsg))
    else:
        bench_folder = SAVED_REPLAY_FOLDER_PATH if use_saved_replay == 'True' else USER_UPLOAD_FOLDER_PATH
        filename_bench = os.path.join(bench_folder, filename_bench)
        filename_own = os.path.join(USER_UPLOAD_FOLDER_PATH, filename_own)

    # validates the replay files as an actual replay that can be parsed.
    try:
        bench_replay_data, own_replay_data = utils.multiprocessMap(
            ReplayData,
            [filename_bench, filename_own],
            MULTIPROCESS,
            MAX_WORKERS)

    except ValueError as e:
        errormsg = str(e)
        return redirect(url_for('index', error=errormsg))

    except Exception as e:
        errormsg = "Unable to read replay file. Error " + str(e)
        return redirect(url_for('index', error=errormsg))

    return render_template(
        ANALYZE_HTML,
        bench_data = bench_replay_data,
        own_data = own_replay_data)
