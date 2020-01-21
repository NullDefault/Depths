'''
Name: Action Menu
Function: UI Element that allows the user to make a selection from a variety of options
Notes:
'''

from source.rendering_files.user_interface.input_handlers.main_action_menu_handler import MainActionMenuHandler
from source.assets.texture_database import textures
from pygame import font
from os.path import join

cursor = textures['menu_cursor']


class ActionMenu:
    def __init__(self, size, actions):
        font.init()
        self.font = font.Font(join('assets', 'fonts', '3Dventure.ttf'), 32)
        self.size = size  # size of the menu in pixels
        self.actions = actions  # Dictionary with all the possible actions. Key is the index, value is the action.
        self.frame = textures['main_action_menu_frame']
        self.cursor = 0
        self.input_master = MainActionMenuHandler(self)

    def render_on(self, surface, loc):
        surface.blit(self.frame, loc)
        for i in range(0, 4):
            if i == 0:
                item_loc = loc[0] + 16, loc[1] + 16
            elif i == 1:
                item_loc = loc[0] + 48 + self.size[0] // 2, loc[1] + 16
            elif i == 2:
                item_loc = loc[0] + 16, loc[1] + 16 + self.size[1] // 2
            elif i == 3:
                item_loc = loc[0] + 48 + self.size[0] // 2, loc[1] + 16 + self.size[1] // 2
            text_render = self.font.render(self.actions[0 + i], False, (0, 0, 0), None)
            surface.blit(text_render, item_loc)

        if self.cursor == 0:
            cursor_loc = loc[0] + 200, loc[1] + 15
        if self.cursor == 1:
            cursor_loc = loc[0] + 132 + self.size[0] // 2, loc[1] + 15
        if self.cursor == 2:
            cursor_loc = loc[0] + 200, loc[1] + 16 + self.size[1] // 2
        if self.cursor == 3:
            cursor_loc = loc[0] + 132 + self.size[0] // 2, loc[1] + 15 + self.size[1] // 2

        surface.blit(cursor, cursor_loc)
