'''
Name: Texture Database
Function: Holds all the textures for the sake of convenience
Notes:
'''


import pygame

textures = {
    # PLAYER GRAPHICS
    'player': pygame.image.load("assets/player.png"),


    # STRUCTURES
    'wall_visible': pygame.image.load("assets/structures/walls/wall_visible.png"),
    'wall_invisible': pygame.image.load("assets/structures/walls/wall_invisible.png"),
    'floor_visible': pygame.image.load("assets/structures/floors/floor_visible.png"),
    'floor_invisible': pygame.image.load("assets/structures/floors/floor_invisible.png"),
    'stairs_down': pygame.image.load("assets/structures/stairs_down.png"),

    # WEAPONS
    'dagger': pygame.image.load("assets/items/weapons/dagger.png"),
    'sword': pygame.image.load("assets/items/weapons/sword.png"),
    'shield': pygame.image.load("assets/items/weapons/shield.png"),

    # ITEMS
    'potion': pygame.image.load("assets/items/potion.png"),
    'scroll': pygame.image.load("assets/items/scroll.png"),

    # ENEMIES
    'orc': pygame.image.load("assets/enemies/orc.png"),
    'troll': pygame.image.load("assets/enemies/troll.png"),

    # MISC
    'corpse': pygame.image.load("assets/misc/corpse.png"),
    'black_bg': pygame.image.load("assets/misc/black_bg.png")
}


def get_sprite(entity_name):
    return textures[entity_name]
