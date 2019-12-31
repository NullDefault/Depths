import pygame

textures = {
    'player': pygame.image.load("assets/player.png"),

    'wall_visible': pygame.image.load("assets/structures/walls/wall_visible.png"),
    'wall_invisible': pygame.image.load("assets/structures/walls/wall_invisible.png"),
    'floor_visible': pygame.image.load("assets/structures/floors/floor_visible.png"),
    'floor_invisible': pygame.image.load("assets/structures/floors/floor_invisible.png"),
    'stairs_down': pygame.image.load("assets/structures/stairs_down.png"),

    'dagger': pygame.image.load("assets/items/weapons/dagger.png"),
    'sword': pygame.image.load("assets/items/weapons/sword.png"),
    'shield': pygame.image.load("assets/items/weapons/shield.png"),
    'potion': pygame.image.load("assets/items/potion.png"),
    'scroll': pygame.image.load("assets/items/scroll.png"),

    'orc': pygame.image.load("assets/enemies/orc.png"),
    'troll': pygame.image.load("assets/enemies/troll.png"),

    'corpse': pygame.image.load("assets/misc/corpse.png")
}


def get_sprite(entity_name):
    return textures[entity_name]
