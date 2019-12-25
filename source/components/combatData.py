class CombatData:
    def __init__(self, hp, defense, attack):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.attack = attack

    def fight(self, target):
        results = []
        damage = self.attack - target.combat_data.defense
        if damage > 0:
            results.append({'message': '{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage))})
            results.extend(target.combat_data.take_damage(damage))
        else:
            results.append({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name)})

        return results

    def take_damage(self, dmg):
        results = []

        self.hp -= dmg

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results
