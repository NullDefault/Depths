'''
Name: Game Map
Function: Holds data on the game map, functions to generate new maps and moving between floors
Notes:
'''

import tcod
from random import randint

from source.game_entities.components.ai import BasicCreature
from source.game_entities.components.combat_data import CombatData
from source.game_entities.components.equippable import Equippable
from source.game_entities.components.item import Item
from source.map_engine.map_rect import MapRect

from source.rendering_files.user_interface.game_messages import Message

from source.data_banks.equipment_slots import EquipmentSlots
from source.data_banks.item_functions import heal, cast_fireball, cast_confuse, cast_lightning

from source.map_engine.tile import Tile

from source.data_banks.render_order import RenderOrder

from source.misc_functions.random_utilities import from_dungeon_level, random_choice_from_dict

from source.game_entities.structures.stairs import Stairs
from source.game_entities.entity import Entity


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):

                wall = self.tiles[x][y].block_sight

                if wall:
                    print('#  ', end='')
                    if x == self.width - 1:
                        print('\n')
                else:
                    print('   ', end='')
                    if x == self.width - 1:
                        print('\n')

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def generate_map(self, max_rooms, min_room_size, max_room_size, map_width, map_height,
                     # TODO: This is bugged and doesnt always fit all the rooms in the tile grid, needs to be fixed
                     player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            w = randint(min_room_size, max_room_size)
            h = randint(min_room_size, max_room_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = MapRect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.generate_room(new_room)

                (new_x, new_y) = new_room.center()  # Center Point

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                    player.move(0, 0)  # To update the player rect as well
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_tunnel_h(prev_x, new_x, prev_y)
                        self.create_tunnel_v(prev_y, new_y, new_x)
                    else:
                        self.create_tunnel_v(prev_y, new_y, prev_x)
                        self.create_tunnel_h(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, 'stairs_down', 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': 55, #from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': 55, #from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':

                    fighter_component = CombatData(hp=20, defense=0, attack=4, xp=35)
                    ai_component = BasicCreature()
                    monster = Entity(x, y, 'orc', 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, combat_data=fighter_component, ai=ai_component)

                else:
                    fighter_component = CombatData(hp=30, defense=2, attack=8, xp=100)
                    ai_component = BasicCreature()

                    monster = Entity(x, y, 'troll', 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, combat_data=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, 'potion', 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, attack_bonus=3)
                    item = Entity(x, y, 'sword', 'Sword', equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, 'shield', 'Shield', equippable=equippable_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', tcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, 'scroll', 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', tcod.light_cyan))
                    item = Entity(x, y, 'scroll', 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, 'scroll', 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def generate_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.create_opening(x, y)

    def create_tunnel_h(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.create_opening(x, y)

    def create_tunnel_v(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.create_opening(x, y)

    def create_opening(self, x, y):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, crosshair, message_log, constants):
        self.dungeon_level += 1
        entities = [player, crosshair]

        self.tiles = self.initialize_tiles()
        self.generate_map(constants['max_rooms'], constants['min_room_size'], constants['max_room_size'],
                          constants['map_width'], constants['map_height'], player, entities)

        player.combat_data.heal(player.combat_data.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', tcod.light_violet))

        return entities
