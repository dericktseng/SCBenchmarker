from sc2reader.factories import SC2Factory
from sc2reader.resources import Replay
from src import utils

def printer(lst):
    i = 0
    for elem in lst:
        print(i, '\t', elem)
        i += 1

def filterfunc(elem):
    return getattr(elem, 'ability', False) and elem.ability.is_build

sc2 = SC2Factory()
replay = sc2.load_replay('./saved-replays/Tri_bunker_rush.SC2Replay', depth=4)
evts = replay.events
gevt = replay.game_events
gevtf = list(filter(filterfunc, gevt))
evtf = list(filter(filterfunc, evts))


def player_names(replay: Replay) -> dict:
    if replay.game_type != '1v1':
        raise ValueError('Game Type is not 1v1')
    playernames = dict()
    for team in replay.teams:
        teamdata = dict([(p.pid, p.name) for p in team.players])
        playernames.update(teamdata)
    return playernames

def init_build_order(replay: Replay) -> dict:
    buildFilter = lambda x: getattr(x, 'ability', False) and x.ability.is_build
    buildOrders = dict([(pid, dict()) for pid in player_names(replay).keys()])

    for builditem in filter(buildFilter, replay.events):
        playerID = builditem.player.pid
        timestamp = builditem.second
        name = builditem.ability_name
        if timestamp not in buildOrders[playerID]:
            buildOrders[playerID][timestamp] = dict()
        playerbuild = buildOrders[playerID][timestamp]
        utils.add_if_key_exists(playerbuild, name, 1)
    return buildOrders
