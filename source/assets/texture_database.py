'''
Name: Texture Database
Function: Holds all the textures for the sake of convenience
Notes:
'''

from os.path import join
from pygame import image

textures = {
    # PLAYER GRAPHICS
    'player': image.load(join('assets', 'player.png')),


    # STRUCTURES
    'wall_visible': image.load(join('assets', 'structures', 'walls', 'wall_visible.png')),
    'wall_invisible': image.load(join('assets', 'structures', 'walls', 'wall_invisible.png')),
    'floor_visible': image.load(join('assets', 'structures', 'floors', 'floor_visible.png')),
    'floor_invisible': image.load(join('assets', 'structures', 'floors', 'floor_invisible.png')),
    'stairs_down': image.load(join('assets', 'structures', 'stairs_down.png')),

    # WEAPONS
    'dagger': image.load(join('assets', 'items', 'weapons', 'dagger.png')),
    'sword': image.load(join('assets', 'items', 'weapons', 'sword.png')),
    'shield': image.load(join('assets', 'items', 'weapons', 'shield.png')),

    # ITEMS
    'potion': image.load(join('assets', 'items', 'potion.png')),
    'scroll': image.load(join('assets', 'items', 'scroll.png')),

    # ENEMIES
    'orc': image.load(join('assets', 'enemies', 'orc.png')),
    'troll': image.load(join('assets', 'enemies', 'troll.png')),

    # MISC
    'corpse': image.load(join('assets', 'misc', 'corpse.png')),
    'black_bg': image.load(join('assets', 'misc', 'black_bg.png')),
    'background': image.load(join('assets', 'ui_elements', 'background.png')),

    # UI
    'console_frame': image.load(join('assets', 'ui_elements', 'console_frame.png')),
    'main_action_menu_frame': image.load(join('assets', 'ui_elements', 'action_menu_frame.png')),
    'inventory_menu_frame': image.load(join('assets', 'ui_elements', 'inventory_menu_frame.png')),
    'inventory_black_bg': image.load(join('assets', 'ui_elements', 'inventory_black_bg.png')),
    'menu_cursor': image.load(join('assets', 'ui_elements', 'menu_cursor.png')),
    'inventory_cursor': image.load(join('assets', 'ui_elements', 'inventory_cursor.png')),
    'xp_bar': image.load(join('assets', 'ui_elements', 'xp_bar.png')),
    'xp_ui': image.load(join('assets', 'ui_elements', 'xp_ui.png')),
    'hp_ui': image.load(join('assets', 'ui_elements', 'hp_ui.png')),
    'heart_full': image.load(join('assets', 'ui_elements', 'status_elements', 'heart_full.png')),
    'heart_half': image.load(join('assets', 'ui_elements', 'status_elements', 'heart_half.png')),
    'heart_empty': image.load(join('assets', 'ui_elements', 'status_elements', 'heart_empty.png'))
}


def get_sprite(entity_name):
    return textures[entity_name]
