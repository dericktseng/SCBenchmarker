from sc2reader.factories import SC2Factory
from sc2reader.events.game import TargetUnitCommandEvent, TargetPointCommandEvent, BasicCommandEvent

def printer(lst):
    i = 0
    for elem in lst:
        print(i, elem)
        i += 1

def filterfunc(elem):
    return (isinstance(elem, TargetUnitCommandEvent) \
            or isinstance(elem, TargetPointCommandEvent) \
            or isinstance(elem, BasicCommandEvent)) \
            and elem.ability_name != 'RightClick' \
            and elem.ability_name != 'HoldPosition' \
            and elem.ability_name != 'Attack' \

sc2 = SC2Factory()
replay = sc2.load_replay('Tri_bunker_rush.SC2Replay', depth=4)
gevt = replay.game_events
gg = list(filter(filterfunc, gevt))
