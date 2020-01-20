'''
Name: Main
Function: Controls the game loop, entering point for the code, classic main stuff (no String[] args tho)
Notes:
'''

import tcod
import pygame

from source.game_entities.entity import get_blocking_entities_at_location

from source.loading_functions.init_new import get_constants, get_game_variables

from source.rendering_files.user_interface.input_functions import process_event
from source.rendering_files.user_interface.game_messages import Message

from source.rendering_files.rendering import recompute_fov, initialize_fov, get_render

from source.misc_functions.death_functions import kill_monster, kill_player

from source.data_banks.game_states import GameStates


def main():
    running = True

    constants = get_constants()

    display = pygame.display.set_mode(constants['screen_size'])

    player, entities, game_map, game_state, console = get_game_variables(constants)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    main_action_menu_active = False
    inventory_active = False
    character_profile_active = False
    game_state = GameStates.PLAYERS_TURN
    next_game_state = None

    game_clock = pygame.time.Clock()
    game_frame_rate = 24

    while running:

        if game_state is not GameStates.PLAYER_DEAD and next_game_state:
            game_state = next_game_state
            next_game_state = None

        game_clock.tick(game_frame_rate)

        e = pygame.event.wait()
        action, mouse_action = process_event(e, game_state)

        if game_state == GameStates.ACTION_MENU:
            menu_action_result = console.handle_am_input(e)
            if menu_action_result is None:
                pass
            elif menu_action_result == 'Inventory':
                inventory_active = True
                game_state = GameStates.INVENTORY_MENU
            elif menu_action_result == 'Save':
                pass
            elif menu_action_result == 'Character':
                pass
            elif menu_action_result == 'Quit':
                running = False
            elif menu_action_result == 'quit_menu':
                main_action_menu_active = not main_action_menu_active
                game_state = GameStates.PLAYERS_TURN

        elif game_state == GameStates.INVENTORY_MENU:
            inventory_selection = console.handle_inventory_input(e)
            if inventory_selection is 'quit_menu':
                inventory_active = False
                game_state = GameStates.ACTION_MENU
            elif inventory_selection:
                temp = player.inventory.use(inventory_selection)
                results = temp[0]
                try:
                    equip = results['equip']
                    equip_result = player.equipment.toggle_equip(equip)

                    for message in equip_result:
                        console.add_message(message)

                    game_state = GameStates.ENEMY_TURN
                    next_game_state = GameStates.INVENTORY_MENU
                except KeyError:
                    equip = None
                try:
                    targeting = results['targeting']
                except KeyError:
                    targeting = None

                try:
                    consumed = results['consumed']

                    console.inventory_menu.decrement_cursor()

                    game_state = GameStates.ENEMY_TURN
                    next_game_state = GameStates.INVENTORY_MENU
                except KeyError:
                    consumed = None

                try:
                    message = results['message']
                    console.add_message(message)
                except KeyError:
                    message = None

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'],
                          constants['fov_light_walls'], constants['fov_algorithm'])

        abstract_game_surface = get_render(entities, game_map, fov_map)
        console_surface = console.render(main_action_menu_active, inventory_active, character_profile_active)

        display.blit(abstract_game_surface, (0, 0))  # Blit game
        display.blit(console_surface, (800, 0))  # Blit console

        pygame.display.flip()
        fov_recompute = False

        move = action.get('move')
        pickup = action.get('pickup')
        take_stairs = action.get('take_stairs')
        fullscreen = action.get('fullscreen')
        wait = action.get('wait')
        menu_mode_changed = action.get('menu_mode_changed')

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

        elif take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, console.message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    break
            else:
                console.add_message(Message('There are no stairs here.', tcod.yellow))

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                console.add_message(Message('There is nothing here to pick up.', tcod.yellow))

        elif menu_mode_changed and game_state == GameStates.PLAYERS_TURN:
            player_turn_results.append({'menu_mode_changed': True})

        elif fullscreen:
            display = pygame.display.set_mode(constants['screen_size'], pygame.FULLSCREEN)

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            menu_mode_changed = player_turn_result.get('menu_mode_changed')
            item_added = player_turn_result.get('item_added')
            xp = player_turn_result.get('xp')

            if message:
                console.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                console.add_message(message)

            if menu_mode_changed:
                main_action_menu_active = not main_action_menu_active
                game_state = GameStates.ACTION_MENU

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if xp:
                leveled_up = player.level.add_xp(xp)
                console.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:
                    console.add_message(Message(
                        'Your battle skills grow stronger! You reached level {0}'.format(
                            player.level.current_level) + '!', tcod.yellow))

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            console.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            console.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN



if __name__ == '__main__':
    main()
