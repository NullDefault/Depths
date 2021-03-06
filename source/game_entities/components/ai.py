'''
Name: AI
Function: Various AI's for controlling the behavior of npc's
Notes:
'''

from random import randint

import tcod

from source.rendering_files.user_interface.game_messages import Message


# Default NPC AI
class BasicCreature:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_a_star(target, entities, game_map)

            elif target.combat_data.hp > 0:
                attack_results = monster.combat_data.fight(target)
                results.extend(attack_results)

        return results


# NPC affected by the confusion status effect
class ConfusedCreature:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    # Note: Take Turn takes target and fov_map as parameters even though it doesn't use them - this is to avoid errors
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), tcod.red)})

        return results
