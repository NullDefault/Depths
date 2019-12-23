import tcod as libtcod
from source import input_master, entity, render_functions
from source.map_engine.game_map import GameMap
from source.render_functions import render_all, clear_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    player = entity.Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = entity.Entity(int(screen_width / 3), int(screen_height / 3), 'G', libtcod.red)
    entities = [npc, player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'untitled roguelike', False)

    console = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(console, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(console, entities)

        action = input_master.handle_keys(key)

        move = action.get('move')
        end_game = action.get('exit')
        full_screen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if end_game:
            return True

        if full_screen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
