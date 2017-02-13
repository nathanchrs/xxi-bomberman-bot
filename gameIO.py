import entity
import json

class GameException(Exception):
    def __init__(self, message):
        self.message = message

class GameState:
    def __init__(self, filepath):
        js = json.load(open(filepath, 'r'))

        self.playerList = []
        self.wallList = []
        self.bombList = []
        self.powerUpList = []

        self.map = [[' ' for j in range(js['MapWidth'])] for i in range(js['MapHeight'])]

        for player in js['RegisteredPlayerEntities']:
            self.playerList.append(entity.Player(player['Name'], player['Key'], player['Points'], player['Killed'], player['BombBag'], player['BombRadius'], locationToTuple(player['Location'])))

        for _singleEntity in js['GameBlocks']:
            for singleEntity in _singleEntity:
                if singleEntity['Entity']:
                    if singleEntity['Entity']['$type'] != 'Domain.Entities.PlayerEntity, Domain':
                        wall = singleEntity['Entity']
                        self.wallList.append(entity.Wall(wall['$type'], locationToTuple(wall['Location'])))

                elif singleEntity['Bomb']:
                    bomb = singleEntity['Bomb']
                    self.bombList.append(entity.Bomb(bomb['BombRadius'], bomb['BombTimer'], bomb['IsExploding'], locationToTuple(bomb['Location'])))

                elif singleEntity['PowerUp']:
                    pUp = singleEntity['PowerUp']
                    self.powerUpList.append(entity.PowerUp(pUp['$type'], locationToTuple(pUp['Location'])))


        for wall in self.wallList:
            if wall.destructible:
                self.setMap(wall.location, '+')
            else:
                self.setMap(wall.location, '#')

    def setMap(self, location, char):
        self.map[location[0]][location[1]] = char

def locationToTuple(location):
    return (location['X'] - 1, location['Y'] - 1)

def setMove(filepath, move):
    possibleMoves = {'DoNothing': -1, 'MoveUp': 1, 'MoveLeft': 2, 'MoveRight': 3, 'MoveDown': 4, 'PlaceBomb': 5, 'TriggerBomb': 6}

    try:
        moveCode = str(possibleMoves[move])
    except (KeyError):
        raise GameException('Wrong movement name')

    with open(filepath, 'w') as f:
        f.write(moveCode + '\r\n')
