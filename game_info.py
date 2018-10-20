from hlt.positionals import Direction
from hlt import constants
import logging
import random


def get_future_ev(current_halite, max_halite):
    two_turn_stay_ev = current_halite * 1 / constants.EXTRACT_RATIO
    two_turn_stay_ev += current_halite * (1 - 1 / constants.EXTRACT_RATIO) * (1 / constants.EXTRACT_RATIO)
    two_turn_move_ev = max_halite * 1 / constants.EXTRACT_RATIO
    two_turn_move_ev -= current_halite * 1 / constants.MOVE_COST_RATIO
    return two_turn_stay_ev, two_turn_move_ev


def get_command(game_map, ship):
    # Get the nearest neighbor positions and check their halite amounts
    best_neighbor_position = None
    best_neighbor_direction = None
    max_halite = 0
    current_halite = game_map[ship.position].halite_amount

    for neighboring_position in ship.position.get_surrounding_cardinals():
        halite_amt = game_map[neighboring_position].halite_amount
        is_occupied = game_map[neighboring_position].is_occupied

        if (best_neighbor_position is None or halite_amt > max_halite) and not is_occupied:
            max_halite = halite_amt
            best_neighbor_position = neighboring_position
            best_neighbor_direction = game_map.naive_navigate(ship, best_neighbor_position)

    if max_halite == 0:
        # We're surrounded by zero. Pick a random direction for now. We should be smarter about picking targets.
        best_neighbor_direction = random.choice([Direction.North, Direction.South, Direction.East, Direction.West])

    if best_neighbor_position is None:
        # We've been trapped? There is no best position after checking all four
        # For now we'll crash to the right to see if we can free up the situation
        best_neighbor_direction = Direction.East

    logging.info('Max halite nearby: {} direction: {}'.format(
        max_halite, Direction.convert(best_neighbor_direction)))
    logging.info('Halite storage is at {}'.format(ship.halite_amount))
    logging.info('Current halite at this position: {}'.format(current_halite))

    two_turn_stay_ev, two_turn_move_ev = get_future_ev(current_halite, max_halite)

    if two_turn_stay_ev > two_turn_move_ev:
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
