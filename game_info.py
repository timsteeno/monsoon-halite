from hlt.positionals import Direction, Position
from hlt import constants
import logging


def get_future_ev(current_halite, max_halite):
    """Given current_halite: the halite at this position, and max_halite: the largest neighboring halite amount,
    return the expected value if the ship stays still for two turns vs moving to the neighbor position.
    Used by ships in get_command to determine a positive EV move over the next two turns."""
    two_turn_stay_ev = current_halite * 1 / constants.EXTRACT_RATIO
    two_turn_stay_ev += current_halite * (1 - 1 / constants.EXTRACT_RATIO) * (1 / constants.EXTRACT_RATIO)
    two_turn_move_ev = max_halite * 1 / constants.EXTRACT_RATIO
    two_turn_move_ev -= current_halite * 1 / constants.MOVE_COST_RATIO
    return two_turn_stay_ev, two_turn_move_ev


def get_structure_list(game_map):
    """Given a game map, return a numpy array object representing whether each cell is a dropoff or shipyard."""
    width = game_map.width
    height = game_map.height
    structure_list = []

    for x in range(height):
        for y in range(width):
            structure = game_map[Position(x, y)].has_structure
            if structure:
                structure_list.append(Position(x,y))
    return structure_list


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

    if best_neighbor_position is None:
        # We've been trapped? There is no best position after checking all four
        # For now we'll crash to the right to see if we can free up the situation
        best_neighbor_direction = Direction.East

#    logging.info('Max halite nearby: {} direction: {}'.format(
#        max_halite, Direction.convert(best_neighbor_direction)))
#    logging.info('Halite storage is at {}'.format(ship.halite_amount))
#    logging.info('Current halite at this position: {}'.format(current_halite))

    two_turn_stay_ev, two_turn_move_ev = get_future_ev(current_halite, max_halite)

    if two_turn_stay_ev > two_turn_move_ev:
        # Better to stay
#        logging.info("I should stay here. EV={} vs {}".format(
#            current_halite * .25 + current_halite * (.75 * .25),
#            max_halite * .25 - current_halite * .1
#        ))
        return ship.stay_still()
    else:
#        logging.info("I should move. EV={} vs {}".format(
#            current_halite * .25 + current_halite * (.75 * .25),
#            max_halite * .25 - current_halite * .1
#        ))
        return ship.move(best_neighbor_direction)
