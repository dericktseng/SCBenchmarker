from sc2reader.factories import SC2Factory
from sc2reader.resources import Replay
from sc2reader.objects import Participant

from .constants import GAME_EVENTS, ALIASES, BLACKLIST
from . import utils


def pid(p: Participant) -> int:
    return p.pid


class ReplayData():
    """Represents the data in a replay. Timestamps are in seconds.

    instance variables:
        build_order - dictionary of {timestamps: {elementNames: count}}
            first in dictionary is the build order of the first player,
            and the second in dictionary is the build order of the second player.
            Example:
            {
                JohnDoeID: {
                    200: { "probe": 2, "stalker": 1, ...},
                    300: { "probe": 1, "gateway": 1, ...}
                    ...
                },
                RandomUserID: {
                    200: { "probe": 2, "stalker": 1},
                    300: { "probe": 1, "gateway": 1}
                    ...
                }
            }
        mineral_rate - dictionary of { timestamps: rate }
            first in list is the mineral rate of the first player,
            and the second in list is the mineral rate of the second player.
            Example:
            {
                JohnDoeID: {
                    200: 100,
                    300: 150,
                    ...
                },
                RandomUserID: {
                    200: 100,
                    300: 200
                    ...
                }
            }
        gas_rate - dictionary of { timestamps: rate }
            first in list is the gas rate of the first player,
            and the second in list is the gas rate of the second player.
            Example:
            {
                JohnDoeID: {
                    200: 100,
                    300: 150,
                    ...
                },
                RandomUserID: {
                    200: 100,
                    300: 200
                    ...
                }
            }
        workers_produced - dict of { timestamps: workersproduced }
            first in dict is the workers produced of first player.
            second in dict is the works produced of the second player.
            Example:
            {
                JohnDoeID: {
                    15: 2,
                    17: 150,
                    ...
                },
                RandomUserID: {
                    200: 100,
                    300: 200
                    ...
                }
            }
        player_names - dict of {pid: player names}.
            e.g. { 1: 'JohnDoe', 2: 'RandomUser' }
    """

    def __init__(self, path_to_replay: str):
        """ Initializes the instance variables. """
        replay = self.__load_replay_file(path_to_replay)

        self.players = self.__init_players(replay)
        self.build_order = self.__init_build_order(replay)
        self.mineral_rate = self.__init_mineral_rate(replay)
        self.gas_rate = self.__init_gas_rate(replay)
        self.workers_produced = self.__init_workers_produce(replay)
        self.total_supply = self.__init_total_supply(replay)


    def __load_replay_file(self, path_to_replay: str) -> Replay:
        """ Loads the replay file with SC2Reader defined by path_to_replay."""
        sc2 = SC2Factory()
        return sc2.load_replay(path_to_replay, load_level=GAME_EVENTS)


    def __init_players(self, replay: Replay) -> dict:
        """ returns dict of { pid: player name } """
        if replay.game_type != '1v1':
            raise ValueError('Game Type is not 1v1')
        playernames = dict()
        for team in replay.teams:
            teamdata = dict([(pid(p), p.name) for p in team.players])
            playernames.update(teamdata)
        return playernames


    def __init_build_order(self, replay: Replay) -> dict:
        buildFilter = lambda x: getattr(x, 'ability', False) and x.ability.is_build
        buildOrders = dict([(pid, dict()) for pid in self.players.keys()])

        for builditem in filter(buildFilter, replay.game_events):
            playerID = pid(builditem.player)
            fps = replay.frames / replay.game_length.seconds
            timestamp = round(builditem.frame / fps)
            name = builditem.ability_name
            if timestamp not in buildOrders[playerID]:
                buildOrders[playerID][timestamp] = dict()
            playerbuild = buildOrders[playerID][timestamp]
            utils.add_if_key_exists(playerbuild, name, 1)
        return buildOrders


    def __init_mineral_rate(self, replay: Replay) -> dict:
        return {}


    def __init_gas_rate(self, replay: Replay) -> dict:
        return {}


    def __init_workers_produce(self, replay: Replay) -> dict:
        return {}


    def __init_total_supply(self, replay: Replay) -> dict:
        return {}
