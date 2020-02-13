"""
Name: Equipment Slots
Function: Where items can be equipped on, pretty self explanatory
Notes:
"""

from enum import Enum, auto


class EquipmentSlots(Enum):
    MAIN_HAND = auto()
    OFF_HAND = auto()
    HEAD = auto()
    TORSO = auto()
    LEGS = auto()
    GLOVES = auto()
    ACCESSORIES = auto()
