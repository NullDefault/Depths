import tcod as libtcod
from enum import Enum

from source.game_states import GameStates
from source.menus import inventory_menu, level_up_menu, character_screen


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(console, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
               screen_width, screen_height, bar_width, bar_height, bar_y, mouse, colors, game_state):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(console, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(console, x, y, colors.get('light_ground'),
                                                            libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(console, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(console, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(console, entity, fov_map, game_map)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.combat_data.hp, player.combat_data.max_hp,
               libtcod.light_red, libtcod.darkest_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, bar_height, 0, 0, bar_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(console, inventory_title, player.inventory, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(console, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (
            entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
