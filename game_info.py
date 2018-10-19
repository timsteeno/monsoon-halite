from hlt.positionals import Direction
from hlt import constants
import random

def get_command(game_map, ship):
    if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
        return ship.move(random.choice([Direction.North, Direction.South, Direction.East, Direction.West]))
    else:
        return ship.stay_still()
