import tcod
from source.data_banks.game_states import GameStates
from source.data_banks.render_order import RenderOrder
from source.user_interface.game_messages import Message


def kill_player(player):
    player.color = tcod.dark_red

    return Message('You died!', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), tcod.orange)

    return death_message
