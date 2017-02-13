class Player:
    def __init__(self, name, key, points, killed, bombBag, bombRadius, location):
        self.name = name
        self.key = key
        self.points = points
        self.killed = killed
        self.bombBag = bombBag
        self.bombRadius = bombRadius
        self.location = location

class Bomb:
    def __init__(self, bombRadius, bombTimer, isExploding, location):
        self.bombRadius = bombRadius
        self.bombTimer = bombTimer
        self.isExploding = isExploding
        self.location = location

class Wall:
    def __init__(self, tipe, location):
        if tipe == 'Domain.Entities.IndestructibleWallEntity, Domain':
            self.destructible = False
        else:
            self.destructible = True

        self.location = location

class PowerUp:
    def __init__(self, tipe, location):
        if tipe == 'Domain.Entities.PowerUps.SuperPowerUp, Domain':
            self.tipe = 'super'
        elif tipe == 'Domain.Entities.PowerUps.BombRaduisPowerUpEntity, Domain':
            self.tipe = 'radius'
        else:
            self.tipe = 'bag'

        self.location = location

    def isSuper(self):
        return self.tipe == 'super'

    def isRadius(self):
        return self.tipe == 'radius'

    def isBag(self):
        return self.tipe == 'bag'
