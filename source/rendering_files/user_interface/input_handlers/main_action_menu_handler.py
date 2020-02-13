"""
Name: Main Action Menu Handler
Function: Handles the logic behind the player interacting with the main action menu
Notes:
"""

from source.rendering_files.user_interface.input_handlers.input_handler import InputHandler


class MainActionMenuHandler(InputHandler):
    def __init__(self, menu):
        InputHandler.__init__(self, menu)

    def process_input(self, key):
        if key == 'return':
            return self.owner.actions[self.owner.cursor]
        elif key == 'up' or key == 'w' or key == '[8]':  # Note : [i] correspond to num pad keys
            self.owner.cursor = self.owner.cursor - 2
        elif key == 'down' or key == 's' or key == '[2]':
            self.owner.cursor = self.owner.cursor + 2
        elif key == 'left' or key == 'a' or key == '[4]':
            self.owner.cursor = self.owner.cursor - 1
        elif key == 'right' or key == 'd' or key == '[6]':
            self.owner.cursor = self.owner.cursor + 1
        elif key == 'escape' or key == 'tab':
            return 'quit_menu'

        if self.owner.cursor == -2:
            self.owner.cursor = len(self.owner.actions) - 2
        elif self.owner.cursor == -1:
            self.owner.cursor = len(self.owner.actions) - 1
        elif self.owner.cursor == len(self.owner.actions):
            self.owner.cursor = 0
        elif self.owner.cursor == len(self.owner.actions) + 1:
            self.owner.cursor = 1
