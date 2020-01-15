from source.user_interface.game_messages import MessageRenderer, MessageLog
from source.assets.texture_database import textures
from pygame import Surface

heart_weight = 10

frame = textures['console_frame']
heart_full = textures['heart_full']
heart_half = textures['heart_half']
heart_empty = textures['heart_empty']


class Console:
    def __init__(self, font_size, player):
        self.message_log = MessageLog(800, 800, 15)
        self.renderer = MessageRenderer(font_size, self.message_log)
        self.player = player

    def add_message(self, message):
        self.message_log.add_message(message)

    def render(self):
        surface = Surface((800, 800))
        surface.blit(frame, (0, 0))
        self.renderer.write_to_console(surface)  # Writes game messages
        self.draw_health(surface)
        return surface

    def draw_health(self, surface):
        total_hearts = self.player.combat_data.max_hp
        current_hp_ratio = self.player.combat_data.hp / heart_weight
        for i in range(total_hearts // heart_weight):
            if current_hp_ratio - i < 0:
                surface.blit(heart_empty, (16 * (i + 2), 400))
            elif current_hp_ratio - i < 1:
                surface.blit(heart_half, (16 * (i + 2), 400))
            else:
                surface.blit(heart_full, (16 * (i + 2), 400))



