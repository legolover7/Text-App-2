import pygame as pyg
pyg.init()

from classes.display import Colors, Fonts
from classes.globals import Globals
from modules.collider import collides_point
from modules.chunk_text import chunk

class InputField():
    def __init__(self, rect, font, default_text="Enter text", increases_upwards=False):
        self.x, self.y, self.width, self.height = rect
        self.default_text = default_text
        self.font = font
        self.text = ""
        self.increases_upwards = increases_upwards


    def draw(self, active):
        # Get the field's text content and set its correct color
        text = self.text if self.text != "" or self == active else self.default_text
        color = Colors.white if self.text != "" else Colors.lighter_gray

        # Split the field's text content by the maximum amount of character able to fit on a single line
        text_lines = chunk(text, content_width=self.width-5, char_width=self.font.size("A")[0])
        # Calculate the extra height that the field should be to account for multiple lines of text
        extra_height = max(0, (len(text_lines) - 1) * (self.font.size("A")[1] + 2))
        
        # Display background
        pyg.draw.rect(Globals.VID_BUFFER, Colors.gray, (self.x, self.y - (extra_height if self.increases_upwards else 0), self.width, self.height + extra_height), border_radius=5)
        pyg.draw.rect(Globals.VID_BUFFER, Colors.dark_gray, (self.x+2, self.y+2 - (extra_height if self.increases_upwards else 0), self.width-4, self.height-4 + extra_height), border_radius=5)

        
        # Display the lines of text
        vertical_offset = -extra_height if self.increases_upwards else 0
        cursor_position = Globals.cursor_position
        
        # Displays cursor if the length of the message is 0
        if len(text_lines) == 0 and (Globals.cursor_frame > Globals.cursor_timeout or (Globals.cursor_frame % Globals.cursor_period < Globals.cursor_period / 2)):
            text_height = self.font.size("A")[1]
            pyg.draw.rect(Globals.VID_BUFFER, Colors.white, (self.x + 4, self.y + vertical_offset + (self.height - text_height)/2, 2, text_height))

        for line in text_lines:
            # Display the current line, and increase the next line's offset
            text_height = self.font.size(line)[1]
            Globals.VID_BUFFER.blit(self.font.render(line, True, color), (self.x + 4, self.y + vertical_offset + (self.height - text_height)/2))
            
            # Draw cursor only on the current line
            if self == active and (Globals.cursor_frame > Globals.cursor_timeout or (Globals.cursor_frame % Globals.cursor_period < Globals.cursor_period / 2)):
                if cursor_position <= len(line):
                    text_width = self.font.size(line[:Globals.cursor_position])[0]
                    pyg.draw.rect(Globals.VID_BUFFER, Colors.white, (self.x + 4 + (text_width), self.y + vertical_offset + (self.height - text_height)/2, 2, text_height))
                else:
                    cursor_position -= len(line)

            vertical_offset += text_height + 2

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))