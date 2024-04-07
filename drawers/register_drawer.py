import pygame as pyg
pyg.init()

from classes.display import Colors, Fonts
from classes.globals import Globals
import drawers.common_drawer as common_drawer
from modules.collider import collides_point

def draw(error_message):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    # Draw title
    common_drawer.draw_text(VID_BUFFER, "Register", Fonts.login_header, Colors.white, (0, 0, WIDTH, 580))

    common_drawer.draw_text(VID_BUFFER, error_message, Fonts.contact_font, Colors.red, (0, 0, WIDTH, 660))

    # Sign up text
    common_drawer.draw_text(VID_BUFFER, "Already have an account? Back to", Fonts.contact_font, Colors.white, (0, 0, WIDTH - 100, 1310))
    text_width, text_height = Fonts.contact_font.size("Login")
    common_drawer.draw_text(VID_BUFFER, "Login", Fonts.contact_font, Colors.light_blue, (0, 0, WIDTH + 330, 1310))
    # Draw underline when hovered
    if collides_point(Globals.mouse_position, ((WIDTH + 330 - text_width)/2, 1310/2 - text_height/2, text_width, text_height)):
        pyg.draw.rect(VID_BUFFER, Colors.light_blue, ((WIDTH + 330 - text_width)/2, 1310/2 + text_height/2, text_width, 2))