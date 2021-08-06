# number of in-game ticks in one second real time
TICKS_PER_SECOND = 22.4

# level of loading required to obtain game event
GAME_EVENTS = 4

# file extension
SC2REPLAY = 'SC2Replay'

# server constants
FLASK_CONFIG = 'config.py'
INDEX_HTML = 'index.html.jinja'
ANALYZE_HTML = 'analyze.html.jinja'
OWN_REPLAY_TAG = 'own_replay'
BENCH_REPLAY_TAG = 'bench_replay'
SAVED_REPLAYS_TAG = 'saved_replay'

# aliases for units in different modes, set to the same unit
ALIASES = {
    # protoss aliases
    'WarpPrismPhasing': 'WarpPrism',
    'WarpGate': 'Gateway',
    'ObserverSiegeMode': 'Observer',

    # zerg aliases
    'OverlordTransport': 'DropperLord',
    'LurkerDenMP': 'LurkerDen',
    'LurkerMP': 'Lurker',
    'SwarmHostMP': 'SwarmHost',

    # terran aliases
    'SiegeTankSieged': 'SiegeTank',
    'SupplyDepotLowered': 'SupplyDepot',
    'LiberatorAG': 'Liberator',
    'ThorAP': 'Thor',
    'WidowMineBurrowed': 'WidowMine',
    'BarracksReactor': 'Reactor',
    'FactoryReactor': 'Reactor',
    'StarportReactor': 'Reactor',
    'FactoryTechLab': 'TechLab',
    'StarportTechLab': 'TechLab',
    'BarracksTechLab': 'TechLab',
    'BarracksFlying': 'Barracks',
    'FactoryFlying': 'Factory',
    'StarportFlying': 'Starport',
    'CommandCenterFlying': 'CommandCenter',
    'OrbitalCommandFlying': 'OrbitalCommand',
    'VikingFighter': 'Viking',
    'VikingAssault': 'Viking',
    'PunisherGrenades': 'ConcussiveShells'
}

# blacklist specific entries from showing up.
BLACKLIST = [
    # Zerg
    'Egg',
    'Larva',
    'CreepTumorBurrowed',
    'RavagerCocoon',
    'CreepTumor',
    'LurkerMPEgg',
    'LocustMP',
    'LocustMPFlying',
    'LocustMPPrecursor',
    'BroodLordCocoon',
    'BroodlingEscort',
    'Broodling',
    'BanelingCocoon',
    'OverlordCocoon',
    'TransportOverlordCocoon',
    'CreepTumorQueen',

    # Terran
    'MULE',

    # Protoss
    'Interceptor'
]
