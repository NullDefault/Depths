"""
Name: Game States
Function: Holds possible states the game loop can be in at a given moment
Notes:
"""

from enum import Enum, auto


class GameStates(Enum):
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    ACTION_MENU = auto()
    INVENTORY_MENU = auto()
    TARGETING = auto()
