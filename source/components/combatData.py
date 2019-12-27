from source.game_messages import Message
import tcod as libtcod


class CombatData:
    def __init__(self, hp, defense, attack, xp=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.xp = xp

    def fight(self, target):
        results = []
        damage = self.attack - target.combat_data.defense
        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.combat_data.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results

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
