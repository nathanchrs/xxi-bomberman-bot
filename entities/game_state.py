class GameState:
    def __init__(self):
        self.round = 0
        self.players = []
        self.walls = []
        self.bombs = []
        self.power_ups = []
        self.map = []

    def set_map(self, location, char):
        self.map[location[0]][location[1]] = char
