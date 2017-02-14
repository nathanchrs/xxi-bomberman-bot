from entities.bomb import Bomb
from entities.player import Player
from entities.power_up import PowerUp
from entities.wall import Wall
from entities.game_state import GameState
from entities.moves import Moves

class GreedyStrategy:
	def __init__(self):
		pass

	def calculate_next_move(self, game_state):
		return Moves.MOVE_DOWN