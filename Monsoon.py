#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
import logging
import game_info


# INITIALIZE

game = hlt.Game()
shipyard_position = game.me.shipyard.position

# Configure the dict for which bots are headed to shipyard
is_depositing = {}
for ship in game.me.get_ships():
    is_depositing[ship.id] = False

# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("Monsoon (Potato)")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

    # Add a move for each ship
    for ship in me.get_ships():
        if ship.position == shipyard_position:
            # We made the deposit. Turn off is_depositing and get a new command
            is_depositing[ship.id] = False

        if ship.halite_amount >= constants.MAX_HALITE*.98:
            # We're full. Set is_depositing so we'll head back.
            is_depositing[ship.id] = True

        if is_depositing[ship.id]:
            # We are depositing but still aren't at the shipyard. Head there.
            command_queue.append(ship.move(game_map.naive_navigate(ship, shipyard_position)))
        else:
            command_queue.append(game_info.get_command(game_map, ship))

    # Decide whether to spawn a new ship
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
