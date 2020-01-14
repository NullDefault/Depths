'''
Name: Render Order
Function: Holds data on the priority in which entities get rendered during gameplay (higher val = higher priority)
Notes:
'''

from enum import Enum


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4
