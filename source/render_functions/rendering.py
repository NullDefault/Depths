import tcod
import pygame

from source.assets.texture_database import textures

RENDER_SCALE = 16  # Corresponds to texture size

wall_visible = textures['wall_visible']
wall_invisible = textures['wall_invisible']
floor_visible = textures['floor_visible']
floor_invisible = textures['floor_invisible']


def get_render(game_screen, entities, game_map, fov_map, fov_recompute):

    entities_to_render = pygame.sprite.RenderUpdates()
    entities_in_render_order = sorted(entities, key=lambda n: n.render_order.value)
    entities_to_render.add(entities_in_render_order)
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):

                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        game_screen.blit(wall_visible, (x * RENDER_SCALE, y * RENDER_SCALE))
                    else:
                        game_screen.blit(floor_visible, (x * RENDER_SCALE, y * RENDER_SCALE))

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        game_screen.blit(wall_invisible, (x * RENDER_SCALE, y * RENDER_SCALE))
                    else:
                        game_screen.blit(floor_invisible, (x * RENDER_SCALE, y * RENDER_SCALE))

    return entities_to_render


def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
