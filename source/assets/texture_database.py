'''
Name: Texture Database
Function: Holds all the textures for the sake of convenience
Notes:
'''

from os.path import join
from pygame import image, display

display = display.set_mode()


def load_img(path):
    path = join('source', 'assets', path)
    return image.load(path).convert_alpha()


textures = {
    # PLAYER GRAPHICS
    'player': load_img('player.png'),


    # STRUCTURES
    'wall_visible': load_img(join('structures', 'walls', 'wall_visible.png')),
    'wall_invisible': load_img(join('structures', 'walls', 'wall_invisible.png')),
    'floor_visible': load_img(join('structures', 'floors', 'floor_visible.png')),
    'floor_invisible': load_img(join('structures', 'floors', 'floor_invisible.png')),
    'stairs_down': load_img(join('structures', 'stairs_down.png')),

    # WEAPONS
    'dagger': load_img(join('items', 'weapons', 'dagger.png')),
    'sword': load_img(join('items', 'weapons', 'sword.png')),
    'shield': load_img(join('items', 'weapons', 'shield.png')),

    # ITEMS
    'potion': load_img(join('items', 'potion.png')),
    'scroll': load_img(join('items', 'scroll.png')),

    # ENEMIES
    'orc': load_img(join('enemies', 'orc.png')),
    'troll': load_img(join('enemies', 'troll.png')),

    # MISC
    'corpse': load_img(join('misc', 'corpse.png')),

    # BACKGROUNDS
    'black_bg': load_img(join('ui_elements', 'backgrounds', 'black_bg.png')),
    'background': load_img(join('ui_elements', 'backgrounds', 'background.png')),
    'inventory_black_bg': load_img(join('ui_elements', 'backgrounds', 'inventory_black_bg.png')),

    # UI FRAMES
    'console_frame': load_img(join('ui_elements', 'ui_frames', 'console_frame.png')),
    'main_action_menu_frame': load_img(join('ui_elements', 'ui_frames', 'action_menu_frame.png')),
    'inventory_menu_frame': load_img(join('ui_elements', 'ui_frames', 'inventory_menu_frame.png')),

    # UI ICONS
    'menu_cursor': load_img(join('ui_elements', 'icons', 'menu_cursor.png')),
    'inventory_cursor': load_img(join('ui_elements', 'icons', 'inventory_cursor.png')),

    'crosshair': load_img(join('ui_elements', 'icons', 'crosshair.png')),

    'off_hand_icon': load_img(join('ui_elements', 'icons', 'off_hand_icon.png')),
    'main_hand_icon': load_img(join('ui_elements', 'icons', 'main_hand_icon.png')),

    'xp_bar': load_img(join('ui_elements', 'icons', 'xp_bar.png')),
    'xp_ui': load_img(join('ui_elements', 'icons', 'xp_ui.png')),
    'hp_ui': load_img(join('ui_elements', 'icons', 'hp_ui.png')),

    'heart_full': load_img(join('ui_elements', 'icons', 'heart_full.png')),
    'heart_half': load_img(join('ui_elements', 'icons', 'heart_half.png')),
    'heart_empty': load_img(join('ui_elements', 'icons', 'heart_empty.png'))
}


def get_sprite(entity_name):
    return textures[entity_name]
