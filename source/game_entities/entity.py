'''
Name: Entity
Function: One of the most important logic classes, holds data on a game entity and a variety of functions necessary
          for its usual behavior.
Notes: x and y are the logical position of the entity on the tile board, rect.left and rect.top are how the entity
       actually gets rendered -> rect position is easily obtained by multiplying x,y by 16 (the size of the textures)
'''

import math
import pygame
import tcod

from source.game_entities.components.item import Item
from source.data_banks.render_order import RenderOrder
from source.assets.texture_database import get_sprite


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None


class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, sprite_name, name, blocks=False, render_order=RenderOrder.CORPSE,
                 combat_data=None,
                 ai=None,
                 item=None,
                 inventory=None,
                 stairs=None,
                 level=None,
                 equipment=None,
                 equippable=None):

        self.name = name

        pygame.sprite.Sprite.__init__(self)

        self.image = get_sprite(sprite_name)
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.rect.left, self.rect.top = (x * 16, y * 16)  # x and y are the entities logical position on the game grid
        self.blocks = blocks  # rect.left and rect.top are the entity render destination
        self.render_order = render_order  # since all textures are 16x16, just multiply x and y by 16

        self.combat_data = combat_data
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable

        if self.combat_data:
            self.combat_data.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.left = self.x * 16
        self.rect.top = self.y * 16

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_a_star(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as un walkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                        not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles The path size matters if
        # you want the monster to use alternative longer paths (for example through other rooms) if for example the
        # player is in a corridor It makes sense to keep path size relatively low to keep the monsters from running
        # around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
                self.move(0, 0)  # This is to make sure the entity rectangle gets updated as well
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster
            # blocks a corridor) it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        tcod.path_delete(my_path)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
