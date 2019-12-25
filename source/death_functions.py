import tcod as libtcod
from source.game_states import GameStates
from source.render_functions import RenderOrder
from source.game_messages import Message


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)

    return death_message
