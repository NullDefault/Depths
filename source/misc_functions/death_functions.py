"""
Name: Death Functions
Function: Collection of functions that handles entity death (through combat or else)
Notes:
"""

import tcod

from source.assets.texture_database import textures
from source.data_banks.game_states import GameStates
from source.data_banks.render_order import RenderOrder
from source.rendering_files.user_interface.game_messages import Message


def kill_player(player):
    player.image = textures['corpse']
    return Message('You died!', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    monster.image = textures['corpse']
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), tcod.orange)

    return death_message
