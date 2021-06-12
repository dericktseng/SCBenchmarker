from zephyrus_sc2_parser import parse_replay
from .constants import TICKS_PER_SECOND, ALIASES, BLACKLIST
from . import utils
import concurrent.futures


def load_replay_file(path_to_replay: str, delta_second: int):
    """ Loads the replay file defined by path_to_replay."""
    deltatick = delta_second * TICKS_PER_SECOND
    return parse_replay(
        path_to_replay,
        local=True,
        tick=deltatick)


def load_replays_as_sc2replay(
        lst: list,
        allow_multiprocess: bool,
        max_workers: int,
        delta_second: int):
    """ loads in a list of paths to sc2replays, and uses
    the zephyrus_sc2_parser on all of them to return the replay object.

    parameters:
        lst - list of replay paths
        allow_multiprocess - whether to use multiprocessing or not
        max_workers - max number of multiprocess workers
        delta_second - time in seconds between polls of the replay
    """
    # uses multiprocess to load in parallel.
    if allow_multiprocess:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(load_replay_file, path, delta_second) for path in lst]
        return [f.result() for f in futures]
    else:
        return [load_replay_file(path, delta_second) for path in lst]


def to_MM_SS(time_in_seconds):
    time_in_seconds = round(time_in_seconds)
    MM = str(time_in_seconds // 60).zfill(2)
    SS = str(time_in_seconds % 60).zfill(2)
    return "{}:{}".format(MM, SS)


def get_timeline_data(replay):
    """ Returns the times from the replay for both players"""
    timeline = replay.timeline
    timeline_data = dict()
    for player in replay.players:
        timeline_data[player] = [
            to_MM_SS(state[player]['gameloop'] / TICKS_PER_SECOND)
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


def get_gas_data(replay):
    """ Returns the gas evolution over time for both players"""
    timeline = replay.timeline
    gas_data = dict()
    for player in replay.players:
        gas_data[player] = [
            state[player]['resource_collection_rate']['gas']
            for state in timeline
        ]
    return gas_data


def get_workers_produced(replay):
    """ Returns the total workers produced at each increment of time """
    timeline = replay.timeline
    workers_data = dict()
    for player in replay.players:
        workers_data[player] = [
            state[player]['workers_produced']
            for state in timeline
        ]
    return workers_data


def get_total_supply(replay):
    """ Returns the timeline total supply of both players """
    timeline = replay.timeline
    supply_data = dict()
    for player in replay.players:
        supply_data[player] = [
            state[player]['supply']
            for state in timeline
        ]
    return supply_data


def get_macro_spells(replay):
    # TODO
    return None


def get_build_order(replay):
    """ Returns the build order for both players of the replay.
    This contains data on the units constructed (alive + dead),
    Upgrades, and buildings constructed (alive + dead).

    format returned:
    {
        1: [{
                "Probe": 5,
                "Stalker": 6,
                "Nexus": 1,
                "CyberneticsCore": 1,
                "upgrades": ["warpgate", "armor1"]
            }, {
                "Probe": 6,
                "Stalker": 7,
                "Nexus": 2,
                "CyberneticsCore": 1,
                "upgrades": ["warpgate", "armor1"]
            },
            ...
            ],
        2: {
            ...
        }
    }
    """
    timeline = replay.timeline
    build_order = dict()
    for player in replay.players:
        build_order_data = list()

        for state in timeline:
            # the dict that contains all of the units, buildings, upgrades,
            # at an instance of time
            current_time_status = dict()

            # units
            units = state[player]['unit']
            unitnames = units.keys()

            # buildings
            buildings = state[player]['building']
            buildingnames = buildings.keys()

            # upgrades
            upgrades = state[player]['upgrade']

            for name in unitnames:
                unitdata = units[name]
                unitcount = unitdata['live'] + unitdata['died'] + unitdata['in_progress']
                if unitcount != 0 and name not in BLACKLIST:
                    utils.add_if_key_exists(
                        current_time_status,
                        ALIASES[name] if name in ALIASES else name,
                        unitcount)

            for name in buildingnames:
                buildingdata = buildings[name]
                buildingcount = buildingdata['live'] + buildingdata['died'] + buildingdata['in_progress']
                if buildingcount != 0 and name not in BLACKLIST:
                    utils.add_if_key_exists(
                        current_time_status,
                        ALIASES[name] if name in ALIASES else name,
                        buildingcount)

            for upgrade in upgrades:
                current_time_status[upgrade] = 1

            build_order_data.append(current_time_status)

        build_order[player] = build_order_data
    return build_order


def get_player_names(replay):
    """ Returns a dictionary of names with corresponding index (1 or 2)
    e.g. {1: "MetriC", 2: "JohnDoe"}
    """
    players = replay.players
    return dict([(key, players[key].name) for key in players])


def dual_data(func, replay1, replay2):
    """ applies function to replay1 and replay2 and returns the data lists
    to have the same length.
    e.g. func(replay1) = {1: [a,b,c,d,e], 2: [a,b,c,d,e]}
         func(replay2) = {1: [1,2,3,4], 2: [1,2,3,4]}
         returns {1: [a,b,c,d], 2: [a,b,c,d]}, {1: [1,2,3,4], 2: [1,2,3,4]}
    """
    data1 = func(replay1)
    data2 = func(replay2)

    """ validates data returned
    1 & 2 of func(replay1) are same types
    1 & 2 of func(replay2) are same types
    types of func(replay1)[1] and func(replay2)[1] are same
    """
    if not isinstance(data1[1], type(data1[2])):
        raise TypeError('Type Mismatch between data in replay1')
    elif not isinstance(data2[1], type(data2[2])):
        raise TypeError('Type Mismatch between data in replay2')
    elif not isinstance(data1[1], type(data2[1])):
        raise TypeError('Type Mismatch between data in replays')
    elif type(data1[1]) is not list:
        return data1, data2
    else:
        # trims the long data to match length of short data
        trimmed_length = min(len(data1[1]), len(data2[1]))

        # data1 and data2 should both have the same players (1 and 2)
        for player in data1:
            data1[player] = data1[player][:trimmed_length]
            data2[player] = data2[player][:trimmed_length]
        return data1, data2
