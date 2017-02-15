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
		
		current_player = filter(lambda player: player.key == self.player_key, game_state.players)[0]
		current_x, current_y = current_player.location

		# Calculate bomb, danger, blast and target zones.
		# - bomb_zones: map of areas that contains a bomb (marked 'x')
		# - danger_zones: map of areas that will be hit by blast (marked 'x').
		# Areas that have a high probability of being blasted in the next turn are marked '*'.
		# - target_zones: map of areas that will probably be blasted by our own bomb (marked 'x').
		# Note: blast area calculation does not consider bomb/player blast blocking/triggering effect.
		bomb_map = copy.deepcopy(game_state.map)
		danger_zones = copy.deepcopy(game_state.map)
		target_zones = copy.deepcopy(game_state.map)

		for bomb in game_state.bombs:
			bomb_x, bomb_y = bomb.location
			bomb_map[bomb_y][bomb_x] = 'x'
			bomb_travel = ['up', 'left', 'right', 'down']
			for i in range(0, bomb.radius+1):
				for direction in bomb_travel:
					check_location = utils.shift(bomb.location, direction, i)
					check_x, check_y = check_location
					if utils.map_equals(danger_zones, check_location, ['.', 'x', '*']):
						danger_zones[check_y][check_x] = 'x'
						if bomb.timer == 1:
							danger_zones[check_y][check_x] = '*'
						if bomb.owner == self.player_key:
							target_zones[check_y][check_x] = 'x'
					elif utils.map_equals(danger_zones, check_location, ['#', '+']):
						bomb_travel.remove(direction)

		# DEBUG
		print '--- Bomb map ---'
		utils.print_map(bomb_map)
		print '--- Danger zones ---'
		utils.print_map(danger_zones)
		print '--- Target zones ---'
		utils.print_map(target_zones)

		# If in danger zone, try to find a path to nearest safe location.
		if utils.map_equals(danger_zones, current_player.location, ['x', '*']):
			path_to_safety = utils.shortest_path(
				map = danger_zones,
				start = current_player.location,
				end_chars = ['.'],
				costs = { '#': -1, '*': -1, '+': -1, 'x': 1, '.': 1 }
			)
			if path_to_safety is None:
				print "It's a trap!" # DEBUG
				if current_player.bomb_bag == 0 or utils.map_equals(bomb_map, current_player.location, ['x']):
					return Moves.TRIGGER_BOMB
				else:
					return Moves.PLACE_BOMB
			else:
				print 'Trying to escape to a safe place...' # DEBUG
				return path_to_safety[0]
		
		# If an enemy player is in the target zone, trigger our bombs - around 50% probability of a kill
		for player in game_state.players:
			if (player.key != current_player.key):
				if utils.map_equals(bomb_map, player.location, ['x']):
					print 'Enemy ' + player.key + ' is probably in target zone, triggering bombs...' # DEBUG
					return Moves.TRIGGER_BOMB
		
		# If placing a bomb will trap enemy, place bomb
		
		# If next to a destructible wall, place bomb
		
		# Try to find a path to nearest accessible power up.
		
		# Try to find a path to the nearest destructible wall.

		# Try to find a path to the nearest enemy.

		# Don't know what else to do
		print "Nothing else to do." # DEBUG
		return Moves.DO_NOTHING