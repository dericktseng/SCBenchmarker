from sc2reader.events.game import TargetUnitCommandEvent, TargetPointCommandEvent, BasicCommandEvent
from sc2reader.factories import SC2Factory
from sc2reader.resources import Replay

from .constants import GAME_EVENTS, ALIASES, BLACKLIST
from . import utils



class ReplayData():
    """Represents the data in a replay. Timestamps are in seconds.

    instance variables:
        build_order - dictionary of {timestamps: {elementNames: count}}
            first in dictionary is the build order of the first player,
            and the second in dictionary is the build order of the second player.
            Example:
            {
                "JohnDoe": {
                    200: { "probe": 2, "stalker": 1, ...},
                    300: { "probe": 1, "gateway": 1, ...}
                    ...
                },
                "RandomUser": {
                    200: { "probe": 2, "stalker": 1},
                    300: { "probe": 1, "gateway": 1}
                    ...
                }
            }
        mineral_rate - list of dictionary of { timestamps: rate }
            first in list is the mineral rate of the first player,
            and the second in list is the mineral rate of the second player.
            Example:
            {
                "JohnDoe": {
                    200: 100,
                    300: 150,
                    ...
                },
                "RandomUser": {
                    200: 100,
                    300: 200
                    ...
                }
            }
        gas_rate - list of dictionary of { timestamps: rate }
            first in list is the gas rate of the first player,
            and the second in list is the gas rate of the second player.
            Example:
            {
                "JohnDoe": {
                    200: 100,
                    300: 150,
                    ...
                },
                "RandomUser": {
                    200: 100,
                    300: 200
                    ...
                }
            }
        workers_produced - list of { timestamps: workersproduced }
            first in dict is the workers produced of first player.
            second in dict is the works produced of the second player.
            Example:
            {
                "JohnDoe": {
                    15: 2,
                    17: 150,
                    ...
                },
                "RandomUser": {
                    200: 100,
                    300: 200
                    ...
                }
            }
        player_names - list of player names.
            e.g. [ 'JohnDoe', 'RandomUser' ]
    """

    def __init__(self, path_to_replay: str):
        """ Initializes the instance variables. """
        replay = self.__load_replay_file(path_to_replay)

        self.player_names = self.__init_player_names(replay)
        self.build_order = self.__init_build_order(replay)
        self.mineral_rate = self.__init_mineral_rate(replay)
        self.gas_rate = self.__init_gas_rate(replay)


    def __load_replay_file(self, path_to_replay: str) -> Replay:
        """ Loads the replay file with SC2Reader defined by path_to_replay."""
        sc2 = SC2Factory()
        return sc2.load_replay(path_to_replay, load_level=GAME_EVENTS)


    def __init_player_names(self, replay: Replay) -> list:
        """ returns list of player names """
        if replay.game_type != '1v1':
            raise ValueError('Game Type is not 1v1')
        playernames = list()
        for team in replay.teams:
            if len(team.players) > 0:
                player = team.players[0].name
                playernames.append(player)
        return playernames


    def __init_build_order(self, replay: Replay) -> dict:
        buildOrders = dict()

        for player in self.player_names:
            buildOrders[player] = None
        return buildOrders


    def __init_mineral_rate(self, replay: Replay) -> dict:
        return {}


    def __init_gas_rate(self, replay: Replay) -> dict:
        return {}


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
                unitcount = unitdata['live'] + unitdata['died']
                if unitcount != 0 and name not in BLACKLIST:
                    utils.add_if_key_exists(
                        current_time_status,
                        ALIASES[name] if name in ALIASES else name,
                        unitcount)

            for name in buildingnames:
                buildingdata = buildings[name]
                buildingcount = buildingdata['live'] + buildingdata['died']
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
