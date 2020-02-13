"""
Name: Inventory Handler
Function: Handles the logic behind the player interacting with the inventory
Notes:
"""

from source.rendering_files.user_interface.input_handlers.input_handler import InputHandler


class InventoryHandler(InputHandler):
    def __init__(self, menu):
        InputHandler.__init__(self, menu)

    def process_input(self, key):
        if key == 'return':
            return self.owner.inventory.items[self.owner.cursor]
        elif key == 'up' or key == 'w' or key == '[8]':  # Note : [i] correspond to num pad keys
            self.owner.cursor = self.owner.cursor - 1
        elif key == 'down' or key == 's' or key == '[2]':
            self.owner.cursor = self.owner.cursor + 1
        elif key == 'escape' or key == 'tab':
            return 'quit_menu'

        if self.owner.cursor == -1:
            self.owner.cursor = len(self.owner.inventory.items) - 1
        elif self.owner.cursor == len(self.owner.inventory.items):
            self.owner.cursor = 0
        elif self.owner.cursor == len(self.owner.inventory.items) + 1:
            self.owner.cursor = 1
