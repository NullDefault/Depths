'''
Name: Texture Database
Function: Holds all the textures for the sake of convenience
Notes:
'''

import os
import pygame

textures = {
    # PLAYER GRAPHICS
    'player': pygame.image.load(os.path.join('assets', 'player.png')),


    # STRUCTURES
    'wall_visible': pygame.image.load(os.path.join('assets', 'structures', 'walls', 'wall_visible.png')),
    'wall_invisible': pygame.image.load(os.path.join('assets', 'structures', 'walls', 'wall_invisible.png')),
    'floor_visible': pygame.image.load(os.path.join('assets', 'structures', 'floors', 'floor_visible.png')),
    'floor_invisible': pygame.image.load(os.path.join('assets', 'structures', 'floors', 'floor_invisible.png')),
    'stairs_down': pygame.image.load(os.path.join('assets', 'structures', 'stairs_down.png')),

    # WEAPONS
    'dagger': pygame.image.load(os.path.join('assets', 'items', 'weapons', 'dagger.png')),
    'sword': pygame.image.load(os.path.join('assets', 'items', 'weapons', 'sword.png')),
    'shield': pygame.image.load(os.path.join('assets', 'items', 'weapons', 'shield.png')),

    # ITEMS
    'potion': pygame.image.load(os.path.join('assets', 'items', 'potion.png')),
    'scroll': pygame.image.load(os.path.join('assets', 'items', 'scroll.png')),

    # ENEMIES
    'orc': pygame.image.load(os.path.join('assets', 'enemies', 'orc.png')),
    'troll': pygame.image.load(os.path.join('assets', 'enemies', 'troll.png')),

    # MISC
    'corpse': pygame.image.load(os.path.join('assets', 'misc', 'corpse.png')),
    'black_bg': pygame.image.load(os.path.join('assets', 'misc', 'black_bg.png')),
    'background': pygame.image.load(os.path.join('assets', 'ui_elements', 'background.png')),

    # UI
    'console_frame': pygame.image.load(os.path.join('assets', 'ui_elements', 'console_frame.png')),
    'heart_full': pygame.image.load(os.path.join('assets', 'ui_elements', 'status_elements', 'heart_full.png')),
    'heart_half': pygame.image.load(os.path.join('assets', 'ui_elements', 'status_elements', 'heart_half.png')),
    'heart_empty': pygame.image.load(os.path.join('assets', 'ui_elements', 'status_elements', 'heart_empty.png'))
}


def get_sprite(entity_name):
    return textures[entity_name]
