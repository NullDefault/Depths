'''
Name: Input Functions
Function: Handles the logic behind processing player inputs
Notes:
'''

import tcod
import pygame
from source.data_banks.game_states import GameStates


def process_event(event, game_state):
    k, m = {}, {}

    if event.type == pygame.MOUSEBUTTONDOWN:  # This should probably use mousebuttonup instead
        m = handle_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0], pygame.mouse.get_pressed()[1])

    if event.type == pygame.KEYDOWN:
        #  print(pygame.key.name(event.key))
        k = handle_keys(pygame.key.name(event.key), game_state)

    return k, m


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    return {}


def handle_mouse(loc, l_pressed, r_pressed):
    if l_pressed:
        return {'left_click': (loc[0], loc[1])}
    elif r_pressed:
        return {'right_click': (loc[0], loc[1])}

    return {}


def handle_player_turn_keys(key):
    # Movement keys
    if key == 'up' or key == 'w' or key == '[8]':  # Note : [i] correspond to num pad keys
        return {'move': (0, -1)}
    elif key == 'down' or key == 's' or key == '[2]':
        return {'move': (0, 1)}
    elif key == 'left' or key == 'a' or key == '[4]':
        return {'move': (-1, 0)}
    elif key == 'right' or key == 'd' or key == '[6]':
        return {'move': (1, 0)}

    elif key == 'q' or key == '[7]':  # Up Left
        return {'move': (-1, -1)}
    elif key == 'e' or key == '[9]':  # Up Right
        return {'move': (1, -1)}
    elif key == 'x' or key == '[1]':  # Down Left
        return {'move': (-1, 1)}
    elif key == 'c' or key == '[3]':  # Down Right
        return {'move': (1, 1)}

    elif key == 'z':
        return {'wait': True}

    elif key == 'f11':
        return {'fullscreen': True}

    elif key == 'space':
        return {'pickup': True}
    elif key == 'tab':
        return {'show_inventory': True}
    elif key == 'shift':
        return {'drop_inventory': True}
    elif key == 'return':
        return {'take_stairs': True}
    elif key == 'h':
        return {'show_character_screen': True}

    elif key == 'escape':
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_targeting_keys(key):
    if key == 'escape':
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    if key == 'tab':
        return {'show_inventory': True}

    if key == 'f11':
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key == 'escape':
        # Exit the menu
        return {'exit': True}

    return {}


def handle_main_menu(key):

    if key == '1':
        return {'new_game': True}
    elif key == '2':
        return {'load_game': True}
    elif key == '3':
        return {'exit': True}

    return {}


def handle_level_up_menu(key):
    if key:

        if key == '1':
            return {'level_up': 'hp'}
        elif key == '2':
            return {'level_up': 'str'}
        elif key == '3':
            return {'level_up': 'def'}

    return {}


def handle_inventory_keys(key):
    print(key)
    index = 0

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_character_screen(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
