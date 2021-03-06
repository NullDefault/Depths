"""
Name: Equippable
Function: Component that is attached onto an item to signify it can be equipped (and thus is equippable)
Notes:
"""


class Equippable:
    def __init__(self, slot, attack_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
