class Player:
    def __init__(self, name):
        self.name = name
        self.win = 0
        self.lose = 0

    def info(self):
        return self.name + ": win (" + str(self.win) + "); lose (" + str(self.lose) + ")"
