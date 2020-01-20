'''
Name: Action Menu
Function: UI Element for interacting with the players inventory
Notes:
'''

from source.user_interface.input_handler import InventoryHandler
from source.assets.texture_database import textures
from pygame import font
from os.path import join

cursor = textures['inventory_cursor']
black_bg = textures['inventory_black_bg']
main_hand_icon = textures['main_hand_icon']
off_hand_icon = textures['off_hand_icon']


class InventoryMenu:
    def __init__(self, inventory, size):
        font.init()
        self.font = font.Font(join('assets', 'fonts', 'gameFont.ttf'), 24)
        self.inventory = inventory
        self.size = size  # size of the menu in pixels
        self.frame = textures['inventory_menu_frame']
        self.cursor = 0
        self.input_master = InventoryHandler(self)

    def render_on(self, surface, loc):
        surface.blit(black_bg, loc)
        i = 0
        surface.blit(self.frame, loc)
        for item in self.inventory.items:
            text_render = self.font.render(item.name, False, (255, 255, 255), None)
            if i < 19:
                img_loc = (30, 420 + 16*i)
            else:
                img_loc = (240, 420 + 16*(i-19))
            surface.blit(item.image, img_loc)
            text_loc = (img_loc[0] + 20, img_loc[1] + 2)
            surface.blit(text_render, text_loc)
            if self.cursor == i:
                cursor_loc = (text_loc[0] + len(item.name)*10, text_loc[1] - 1)
                surface.blit(cursor, cursor_loc)
            if item is self.inventory.owner.equipment.main_hand:
                icon_loc = (text_loc[0] + 90, text_loc[1] - 1)
                surface.blit(main_hand_icon, icon_loc)
            elif self.inventory.owner.equipment.off_hand == item:
                icon_loc = (cursor_loc[0] + 20, cursor_loc[1])
                surface.blit(off_hand_icon, icon_loc)

            i = i + 1

    def decrement_cursor(self):
        self.cursor = self.cursor - 1
        if self.cursor < 0:
            self.cursor = 0

