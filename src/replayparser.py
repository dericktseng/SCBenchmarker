from zephyrus_sc2_parser import parse_replay
from .constants import TICKS_PER_SECOND
from .config import DELTA_SECOND


def load_replay_file(path_to_replay: str):
    """ Loads the replay file defined by path_to_replay
    """
    deltatick = DELTA_SECOND * TICKS_PER_SECOND
    return parse_replay(
        path_to_replay,
        local=True,
        tick=deltatick)


def get_timeline_data(replay):
    """ Returns the times from the replay for both players"""
    timeline = replay.timeline
    timeline_data = dict()
    for player in replay.players:
        timeline_data[player] = [
            round(state[player]['gameloop'] / TICKS_PER_SECOND)
            for state in timeline
        ]
    return timeline_data


def get_mineral_data(replay):
    """ Returns the mineral evolution over time for both players"""
    timeline = replay.timeline
    mineral_data = dict()
    for player in replay.players:
        mineral_data[player] = [
            state[player]['resource_collection_rate']['minerals']
            for state in timeline
        ]
    return mineral_data


def get_player_names(replay):
    """ Returns a dictionary of names with corresponding index (1 or 2) """
    players = replay.players
    return dict([(players[key].name, key) for key in players])
