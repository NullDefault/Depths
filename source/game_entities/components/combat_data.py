"""
Name: Combat Data
Function: Component that takes care of combat functionality and holds combat related data
Notes:
"""

import tcod

from source.rendering_files.user_interface.game_messages import Message


class CombatData:
    def __init__(self, hp, defense, attack, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_attack = attack
        self.xp = xp

    def fight(self, target):
        results = []
        damage = self.attack - target.combat_data.defense
        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            results.extend(target.combat_data.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), tcod.white)})

        return results

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def attack(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.attack_bonus
        else:
            bonus = 0

        return self.base_attack + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, dmg):
        results = []

        self.hp -= dmg

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
