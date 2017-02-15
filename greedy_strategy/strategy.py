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
		# Note: blast area calculation does not consider bomb/player blast cascade effect.
		danger_zones = copy.deepcopy(game_state.map)
		target_zones = copy.deepcopy(game_state.map)

		for bomb in game_state.bombs:
			bomb_x, bomb_y = bomb.location
			danger_zones[bomb_y][bomb_x] = 'b'
			bomb_travel = ['up', 'left', 'right', 'down']
			for i in range(0, bomb.radius+1):
				for direction in bomb_travel:
					check_location = utils.shift(bomb.location, direction, i)
					check_x, check_y = check_location
					if utils.map_equals(danger_zones, check_location, ['.', 'x']):
						danger_zones[check_y][check_x] = 'x'
						if bomb.timer == 1:
							danger_zones[check_y][check_x] = '*'
						if bomb.owner == self.player_key:
							target_zones[check_y][check_x] = 'x'
					elif utils.map_equals(danger_zones, check_location, ['#', '+']):
						bomb_travel.remove(direction)

		# Create power up map from danger zones map.
		power_up_map = copy.deepcopy(danger_zones)
		for power_up in game_state.power_ups:
			power_up_x, power_up_y = power_up.location
			if utils.map_equals(power_up_map, power_up.location, ['.']):
				power_up_map[power_up_y][power_up_x] = 'p'

		# Create enemy map from danger zones map.
		enemy_map = copy.deepcopy(danger_zones)
		for player in game_state.players:
			if player.key != current_player.key:
				enemy_x, enemy_y = player.location
				if utils.map_equals(enemy_map, player.location, ['.']):
					enemy_map[enemy_y][enemy_x] = 'e'

		# DEBUG
		print '--- Danger zones ---'
		utils.print_map(danger_zones)
		print '--- Target zones ---'
		utils.print_map(target_zones)
		print '--- Power up map ---'
		utils.print_map(power_up_map)
		print '--- Enemy map ---'
		utils.print_map(enemy_map)

		# If in danger zone, try to find a path to nearest safe location.
		if utils.map_equals(danger_zones, current_player.location, ['x', '*', 'b']):
			path_to_safety = utils.shortest_path(
				map = danger_zones,
				start = current_player.location,
				end_chars = ['.'],
				costs = { '#': -1, '*': -1, 'b': -1, '+': -1, 'x': 1, '.': 1 }
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
		# Does not consider blast cascade effect
		for player in game_state.players:
			if (player.key != current_player.key):
				if utils.map_equals(danger_zones, player.location, ['b']):
					print 'Enemy ' + player.key + ' is probably in target zone, triggering bombs...' # DEBUG
					return Moves.TRIGGER_BOMB
		
		# If placing a bomb will trap enemy, place bomb
		# TODO
		
		# If next to a destructible wall, place bomb or trigger if bomb not available yet
		for direction in ['up', 'left', 'right', 'down']:
			if utils.map_equals(game_state.map, utils.shift(current_player.location, direction), ['+']):
				if current_player.bomb_bag > 0:
					print 'Placing bomb to destroy destructible wall...' # DEBUG
					return Moves.PLACE_BOMB
				else:
					print 'Trying to destroy destructible wall; triggering bomb to reload bomb bag...' # DEBUG
					return Moves.TRIGGER_BOMB

		# Try to find a path to nearest accessible power up.
		path_to_power_up = utils.shortest_path(
			map = power_up_map,
			start = current_player.location,
			end_chars = ['p'],
			costs = { '#': -1, '*': -1, 'b': -1, '+': 3, 'x': 30, '.': 1, 'p': 1 }
		)
		if not (path_to_power_up is None):
			print 'Seeking power up...' # DEBUG
			return path_to_power_up[0]

		# Try to find a path to the nearest enemy.
		path_to_enemy = utils.shortest_path(
			map = enemy_map,
			start = current_player.location,
			end_chars = ['e'],
			costs = { '#': -1, '*': -1, 'b': -1, '+': 3, 'x': -1, '.': 1, 'e': 1 }
		)
		if not (path_to_enemy is None):
			print 'Homing in to enemy...' # DEBUG
			return path_to_enemy[0]

		# Try to find a path to the nearest destructible wall.
		path_to_destructible_wall = utils.shortest_path(
			map = game_state.map,
			start = current_player.location,
			end_chars = ['+'],
			costs = { '#': -1, '+': 1, '.': 1 }
		)
		if path_to_destructible_wall is not None:
			print 'Homing in to destructible wall...' # DEBUG
			return path_to_destructible_wall[0]

		# Don't know what else to do
		print "Nothing else to do." # DEBUG
		return Moves.DO_NOTHING