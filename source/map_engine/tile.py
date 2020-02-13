"""
Name: Tile
Function: Represents a single game tile, the width and height are equal to whatever size the textures being used are
Notes:
"""


class Tile:

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
