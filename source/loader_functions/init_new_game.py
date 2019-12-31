import tcod as libtcod
from source.components.combatData import CombatData
from source.components.equipment import Equipment
from source.components.equippable import Equippable
from source.components.inventory import Inventory
from source.components.level import Level
from source.entity import Entity
from source.equipment_slots import EquipmentSlots
from source.game_messages import MessageLog
from source.game_states import GameStates
from source.map_engine.game_map import GameMap
from source.rendering.render_functions import RenderOrder


def get_constants():
    window_title = 'Depths_Game'

    # NEW VARS                                  #
    screen_size = (1024, 768)
    map_width = 768
    map_height = 768

    max_room_size = 256
    min_room_size = 64
    max_rooms = 5

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    constants = {
        'window_title': window_title,
        'screen_size': screen_size,
        'map_width': map_width,
        'map_height': map_height,
        'max_room_size': max_room_size,
        'min_room_size': min_room_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
    }

    return constants


def get_game_variables(constants):

    fighter_component = CombatData(hp=100, defense=1, attack=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()

    player = Entity(0, 0, 'player', 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    combat_data=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, attack_bonus=2)
    dagger = Entity(0, 0, 'dagger', 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.generate_map(constants['max_rooms'], constants['min_room_size'], constants['max_room_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(0, 0, 0)

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state