from zephyrus_sc2_parser import parse_replay
from .constants import DELTA_SECOND
from .constants import TICKS_PER_SECOND


def load_replay_file(path_to_replay: str):
    """ Loads the replay file defined by path_to_replay
    """
    deltatick = DELTA_SECOND * TICKS_PER_SECOND
    return parse_replay(
        path_to_replay,
        local=True,
        tick=deltatick)


def get_timeline_data(replay):
    """ Returns the timeline data from the replay
    """

    # Debugging stuff. Remove when complete.
    timeline = replay.timeline
    game_times_seconds = [elem[1]['gameloop']/TICKS_PER_SECOND for elem in timeline]
