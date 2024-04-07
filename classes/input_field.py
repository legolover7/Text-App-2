import pygame as pyg
pyg.init()

from classes.display import Colors, Fonts
from classes.globals import Globals
from modules.collider import collides_point

class InputField():
    def __init__(self, rect, font, default_text="Enter text"):
        self.x, self.y, self.width, self.height = rect
        self.default_text = default_text
        self.font = font
        self.text = ""


    def draw(self, active):
        pyg.draw.rect(Globals.VID_BUFFER, Colors.gray, (self.x, self.y, self.width, self.height), border_radius=5)
        pyg.draw.rect(Globals.VID_BUFFER, Colors.dark_gray, (self.x+2, self.y+2, self.width-4, self.height-4), border_radius=5)

        text = self.text if self.text != "" or self == active else self.default_text
        color = Colors.white if self.text != "" else Colors.lighter_gray
        
        text_height = self.font.size(text)[1]
        Globals.VID_BUFFER.blit(self.font.render(text, True, color), (self.x + 4, self.y + (self.height - text_height)/2))

        if self == active:
            text_width = self.font.size(text[:Globals.cursor_position])[0]
            pyg.draw.rect(Globals.VID_BUFFER, Colors.white, (self.x + 4 + (text_width), self.y + (self.height - text_height)/2, 2, text_height))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))