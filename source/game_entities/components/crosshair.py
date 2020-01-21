'''
Name: Crosshair
Function: Entity used for taking inputs when using targeting items
Notes:
'''


class Crosshair:
    def __init__(self, player):
        self.player = player

    def update_crosshair(self):
        print(self.owner)
        self.owner.x = self.player.x
        self.owner.y = self.player.y