import tcod as libtcod
import pygame
from enum import Enum


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


wall_visible = pygame.image.load("assets/structures/Walls/wall_visible.png")
wall_invisible = pygame.image.load("assets/structures/Walls/wall_invisible.png")
floor_visible = pygame.image.load("assets/structures/Floors/floor_visible.png")
floor_invisible = pygame.image.load("assets/structures/Floors/floor_invisible.png")


def get_render(game_screen, entities, game_map, fov_map, fov_recompute):

    entities_to_render = pygame.sprite.RenderUpdates()
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    entities_to_render.add(entities_in_render_order)

    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):

                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        game_screen.blit(wall_visible, (x, y))
                    else:
                        game_screen.blit(floor_visible, (x, y))

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        game_screen.blit(wall_invisible, (x, y))
                    else:
                        game_screen.blit(floor_invisible, (x, y))

    return entities_to_render

def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)


