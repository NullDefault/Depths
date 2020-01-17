'''
Name: Game States
Function: Holds possible states the game loop can be in at a given moment
Notes:
'''

from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    ACTION_MENU = 4

