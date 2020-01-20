'''
Name: Equipment
Function: Components that holds data about items an entity is "using" such as a sword, shield or something like that
Notes:
'''

from source.data_banks.equipment_slots import EquipmentSlots
from source.user_interface.game_messages import Message
import tcod


class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def attack_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.attack_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.attack_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append(Message(('Dequipped ' + equippable_entity.name), tcod.lighter_blue))
            else:
                if self.main_hand:
                    results.append(Message(('Dequipped ' + self.main_hand.name), tcod.lighter_blue))

                self.main_hand = equippable_entity
                results.append(Message(('Equipped ' + equippable_entity.name), tcod.lighter_blue))
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append(Message(('Dequipped ' + equippable_entity.name), tcod.lighter_blue))
            else:
                if self.off_hand:
                    results.append(Message(('Dequipped ' + self.off_hand.name), tcod.lighter_blue))

                self.off_hand = equippable_entity
                results.append(Message(('Equipped ' + equippable_entity.name), tcod.lighter_blue))

        return results
