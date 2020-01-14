'''
Name: Equipment Slots
Function: Where items can be equipped on, pretty self explanatory
Notes:
'''

from enum import Enum


class EquipmentSlots(Enum):
    MAIN_HAND = 1
    OFF_HAND = 2
    HEAD = 3
    TORSO = 4
    LEGS = 5
    GLOVES = 6
    ACCESSORIES = 7
