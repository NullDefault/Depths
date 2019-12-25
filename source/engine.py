import tcod as libtcod

from source import input_master, entity, render_functions
from source.entity import get_blocking_entities_at_location
from source.game_states import GameStates
from source.map_engine.game_map import GameMap
from source.components.combatData import CombatData
from source.death_functions import kill_monster, kill_player
from source.render_functions import RenderOrder


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    max_room_size = 10
    min_room_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True

    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }
    player_stats = CombatData(hp=10, defense=2, attack=5)
    player = entity.Entity(0, 0, '@', libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR, combat_data=player_stats)
    entities = [player]

    libtcod.console_set_custom_font('assets/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'untitled roguelike', False)

    console = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.generate_map(max_rooms, min_room_size, max_room_size, map_width, map_height,
                          player, entities, max_monsters_per_room)
    fov_map = render_functions.initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            render_functions.recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_functions.render_all(console, entities, player, game_map,
                                    fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        libtcod.console_flush()

        render_functions.clear_all(console, entities)

        action = input_master.handle_keys(key)

        move = action.get('move')
        end_game = action.get('exit')
        full_screen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.combat_data.fight(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

            game_state = GameStates.ENEMY_TURN

        if end_game:
            return True

        if full_screen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for instance in entities:
                if instance.ai:
                    enemy_turn_results = instance.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:

                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
