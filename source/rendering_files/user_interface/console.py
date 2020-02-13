"""
Name: Console
Function: Contains functions necessary to render UI elements on the screen, including game messages, menu and stats
Notes:
"""

from source.rendering_files.user_interface.game_messages import MessageRenderer, MessageLog
from source.rendering_files.user_interface.menus.action_menu import ActionMenu
from source.rendering_files.user_interface.menus.inventory_menu import InventoryMenu
from source.assets.texture_database import textures
import tcod
from pygame import Surface, draw, key, KEYDOWN

frame = textures['console_frame']
console_size = (800, 800)
frame_loc = (0, 0)

xp_ui = textures['xp_ui']
xp_loc = (35, 430)
xp_frame = textures['xp_bar']
xp_frame_loc = (64, 429)

hp_ui = textures['hp_ui']
hp_loc = (35, 400)

heart_weight = 10
heart_y_loc = 397
heart_full = textures['heart_full']
heart_half = textures['heart_half']
heart_empty = textures['heart_empty']

main_action_menu_size = (400, 150)
main_actions = {
    0: 'Inventory',
    1: 'Save',
    2: 'Character',
    3: 'Quit'
}
main_action_menu_loc = (32, 464)

inventory_menu_size = (400, 500)
inventory_menu_loc = (16, 392)

profile_menu_size = (400, 500)
profile_loc = (32, 464)


class Console:
    def __init__(self, font_size, player):
        self.message_log = MessageLog(800, 800, 15)
        self.main_action_menu = ActionMenu(main_action_menu_size, main_actions)
        self.inventory_menu = InventoryMenu(player.inventory, inventory_menu_size)
        self.renderer = MessageRenderer(font_size, self.message_log)
        self.player = player

    def add_message(self, message):
        self.message_log.add_message(message)

    def handle_am_input(self, e):
        ship_back = None
        if e.type == KEYDOWN:
            ship_back = self.main_action_menu.input_master.process_input(key.name(e.key))
        if ship_back:
            return ship_back

    def handle_inventory_input(self, e):
        ship_back = None
        if e.type == KEYDOWN:
            ship_back = self.inventory_menu.input_master.process_input(key.name(e.key))
        if ship_back:
            return ship_back

    def render(self, action_menu_active, inventory_active, profile_active):
        surface = Surface(console_size)
        surface.blit(frame, frame_loc)
        surface.blit(hp_ui, hp_loc)
        surface.blit(xp_ui, xp_loc)
        self.renderer.write_to_console(surface)  # Writes game messages
        if not inventory_active and not profile_active:
            self.draw_health(surface)
            self.draw_xp(surface)
        if action_menu_active:
            self.main_action_menu.render_on(surface, main_action_menu_loc)

        if inventory_active:
            self.inventory_menu.render_on(surface, inventory_menu_loc)
        elif profile_active:
            self.character_profile.render_on(surface, profile_loc)

        return surface

    def draw_health(self, surface):
        total_hearts = self.player.combat_data.max_hp
        current_hp_ratio = self.player.combat_data.hp / heart_weight

        for i in range(total_hearts // heart_weight):
            if current_hp_ratio - i < 0:
                surface.blit(heart_empty, (16 * (i + 4), heart_y_loc))
            elif current_hp_ratio - i < 1:
                surface.blit(heart_half, (16 * (i + 4), heart_y_loc))
            else:
                surface.blit(heart_full, (16 * (i + 4), heart_y_loc))

    def draw_xp(self, surface):
        surface.blit(xp_frame, xp_frame_loc)

        current_xp = self.player.level.current_xp
        xp_to_next_lvl = self.player.level.experience_to_next_level

        percent = current_xp / xp_to_next_lvl
        if percent == 0:
            return 0

        xp_bar_start = xp_frame_loc[0] + 3, xp_frame_loc[1] + 6

        xp_bar_end_x = xp_bar_start[0] + ((224 - xp_bar_start[0]) * percent)
        xp_bar_end = (xp_bar_end_x, xp_bar_start[1])

        draw.line(surface, tcod.light_green, xp_bar_start, xp_bar_end, 2)



