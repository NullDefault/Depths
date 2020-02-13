"""
Name: Game Messages
Function: Classes that hold data and functions for managing game console messages
Notes:
"""

from os.path import join
from textwrap import wrap

import tcod
from pygame import font


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color  # Stored as Color(R, G, B)


class MessageLog:
    def __init__(self, width, height, max_msgs):
        self.messages = []
        self.width = width
        self.height = height
        self.max = max_msgs
        self.max_msg_len = 44  # the console can fit 44 chars in a single line

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = wrap(message.text, self.max_msg_len)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.max:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))


class MessageRenderer:
    def __init__(self, font_size, message_log):
        self.log = message_log
        font.init()
        self.font = font.Font(join('assets', 'fonts', 'gameFont.ttf'), font_size)

    def write_to_console(self, surface):
        i = 0
        for message in self.log.messages:
            text_render = self.font.render(message.text, False, message.color, None)
            surface.blit(text_render, (32, 32 + i*24))
            i = i + 1
        return surface
