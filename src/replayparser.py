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
    return dict([(key, players[key].name) for key in players])


def dual_data(func, replay1, replay2):
    """ applies function to replay1 and replay2 and returns the data lists
    to have the same length.
    e.g. func(replay1) = {1: [a,b,c,d,e], 2: [a,b,c,d,e]}
         func(replay2) = {1: [1,2,3,4], 2: [1,2,3,4]}
         returns {1: [a,b,c,d], 2: [a,b,c,d]}, {1: [1,2,3,4], 2: [1,2,3,4]}
    """
    shortData = func(replay1)
    longData = func(replay2)
    swapped = False

    if type(shortData[1]) is not type(longData[1]):
        raise TypeError('Type Mismatch between data in replays')
    elif type(shortData[1]) is not list:
        return shortData, longData
    else:
        # trims the long data to match length of short data
        if len(shortData[1]) > len(longData[1]):
            shortData, longData = longData, shortData
            swapped = True

        for player in longData:
            longData[player] = longData[player][:len(shortData[1])]

        if swapped:
            return longData, shortData
        else:
            return shortData, longData
