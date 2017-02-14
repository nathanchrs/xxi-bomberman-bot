import copy
from entities.bomb import Bomb
from entities.player import Player
from entities.power_up import PowerUp
from entities.wall import Wall
from entities.game_state import GameState
from entities.moves import Moves
from greedy_strategy import utils

class GreedyStrategy:

	# Initialize GreedyStrategy with the specified options.
	def __init__(self, player_key):
		self.player_key = player_key

	# Strategy core; given the current game state, return a move to make.
	def calculate_next_move(self, game_state):
		
		map_width = len(game_state.map[0])
		map_height = len(game_state.map)

		# Calculate danger, blast and target zones

		danger_zones = copy.deepcopy(game_state.map)
		blast_zones = copy.deepcopy(game_state.map)
		target_zones = copy.deepcopy(game_state.map)

		for bomb in game_state.bombs:
			bomb_x, bomb_y = bomb.location
			bomb_travel = ['up', 'left', 'right', 'down']
			for i in range(0, bomb.radius+1):
				for direction in bomb_travel:
					check_location = utils.shift(bomb.location, direction, i)
					check_x, check_y = check_location
					if utils.map_equals(danger_zones, check_location, ['.', 'x']):
						danger_zones[check_y][check_x] = 'x'
						if bomb.timer == 1:
							blast_zones[check_y][check_x] = 'x'
						if bomb.owner == self.player_key:
							target_zones[check_y][check_x] = 'x'
					elif utils.map_equals(danger_zones, check_location, ['#', '+']):
						bomb_travel.remove(direction)

		# DEBUG
		print '--- Danger zones ---'
		utils.print_map(danger_zones)
		print '--- Blast zones ---'
		utils.print_map(blast_zones)
		print '--- Target zones ---'
		utils.print_map(target_zones)

		# If in danger zone, try find a path to nearest safe location.
		# If not possible (trapped), place bomb, then trigger
		
		# If an enemy player is in the target zone, trigger our bombs
		
		# If placing a bomb will trap enemy, place bomb
		
		# If next to a destructible wall, place bomb
		
		# Try to find a path to nearest accessible power up.
		
		# Try to find a path to the nearest destructible wall.
		# If there's none, try to find a path to nearest enemy instead.

		# Don't know what else to do
		return Moves.DO_NOTHING