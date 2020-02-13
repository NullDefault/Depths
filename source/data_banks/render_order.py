"""
Name: Render Order
Function: Holds data on the priority in which entities get rendered during gameplay (higher val = higher priority)
Notes:
"""

from enum import Enum, auto


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
    CROSSHAIR = auto()
