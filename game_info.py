from hlt.positionals import Direction
from hlt import constants
import logging

def get_command(game_map, ship):
    # Get the nearest neighbor positions and check their halite amounts
    best_neighbor_position = None
    best_neighbor_direction = None
    max_halite = 0
    current_halite = game_map[ship.position].halite_amount

    for neighboring_position in ship.position.get_surrounding_cardinals():
        halite_amt = game_map[neighboring_position].halite_amount
        if best_neighbor_position is None or halite_amt > max_halite:
            max_halite = halite_amt
            best_neighbor_position = neighboring_position
            best_neighbor_direction = game_map.naive_navigate(ship, best_neighbor_position)

    logging.info('Max halite nearby: {} direction: {}'.format(
        max_halite, Direction.convert(best_neighbor_direction)))
    logging.info('Halite storage is at {}'.format(ship.halite_amount))
    logging.info('Current halite at this position: {}'.format(current_halite))

    if (current_halite * .25 + current_halite * (.75 * .25)) > (max_halite * .25 - current_halite * .1):
        # Better to stay
        logging.info("I should stay here. EV={} vs {}".format(
            current_halite * .25 + current_halite * (.75 * .25),
            max_halite * .25 - current_halite * .1
        ))
        return ship.stay_still()
    else:
        logging.info("I should move. EV={} vs {}".format(
            current_halite * .25 + current_halite * (.75 * .25),
            max_halite * .25 - current_halite * .1
        ))
        return ship.move(best_neighbor_direction)
