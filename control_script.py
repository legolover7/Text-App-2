# Import statements
import pygame as pyg
import sys
import os

# Custom modules
from classes.globals import Globals

# Pages
from pages.login import Login
from pages.texting import Texting
from pages.register import Register

# Initialize window
pyg.init()
info_object = pyg.display.Info()
Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
pyg.display.set_caption("Texting App")
os.system("cls")

map = {
    "Login": Login,
    "Register": Register,
    "Texting": Texting
}

if __name__ == "__main__":
    return_value = Login()
    while True:
        # Reset values
        Globals.cursor_position = 0

        return_value = map[return_value]()