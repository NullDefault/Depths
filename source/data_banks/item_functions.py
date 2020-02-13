"""
Name: Item Functions
Function: Holds functions representing the functionality of various items
Notes:
"""

import tcod

from source.game_entities.components.ai import ConfusedCreature
from source.rendering_files.user_interface.game_messages import Message


def heal(entity, amount):
    results = []

    if entity.combat_data.hp == entity.combat_data.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity.combat_data.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', tcod.green)})

    return results


def cast_lightning(caster, entities, fov_map, damage, maximum_range):
    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.combat_data and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append(
            {'consumed': True, 'target': target, 'message':
                Message('A lighting bolt strikes the {0} with a loud thunder! The damage is {1}'.format(target.name,
                                                                                                        damage))})
        results.extend(target.combat_data.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message':
                        Message('No enemy is close enough to strike.', tcod.red)})

    return results


def cast_fireball(entities, fov_map, damage, radius, target):
    target_x = target[0]
    target_y = target[1]

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    results.append({'consumed': True,
                    'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius),
                                       tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.combat_data:
            results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage),
                                               tcod.orange)})
            results.extend(entity.combat_data.take_damage(damage))

    return results


def cast_confuse(entities, fov_map, target):
    target_x = target[0]
    target_y = target[1]

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedCreature(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message(
                'The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name),
                tcod.light_green)})

            break
    else:
        results.append(
            {'consumed': False, 'message': Message('There is no targetable enemy at that location.', tcod.yellow)})

    return results
