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
    common_drawer.draw_text(VID_BUFFER, "Texting App v2", Fonts.login_header, Colors.aqua, (0, 0, WIDTH, 300))
    common_drawer.draw_text(VID_BUFFER, "By legolover7", Fonts.login_header_2, Colors.aqua, (0, 0, WIDTH, 420))

    common_drawer.draw_text(VID_BUFFER, "Login", Fonts.login_header, Colors.white, (0, 0, WIDTH, 700))

    common_drawer.draw_text(VID_BUFFER, error_message, Fonts.contact_font, Colors.red, (0, 0, WIDTH, 850))

    # Sign up text
    common_drawer.draw_text(VID_BUFFER, "Don't have an account yet?", Fonts.contact_font, Colors.white, (0, 0, WIDTH - 100, 1310))
    text_width, text_height = Fonts.contact_font.size("Sign Up")
    common_drawer.draw_text(VID_BUFFER, "Sign Up", Fonts.contact_font, Colors.light_blue, (0, 0, WIDTH + 280, 1310))
    # Draw underline when hovered
    if collides_point(Globals.mouse_position, ((WIDTH + 280 - text_width)/2, 1310/2 - text_height/2, text_width, text_height)):
        pyg.draw.rect(VID_BUFFER, Colors.light_blue, ((WIDTH + 280 - text_width)/2, 1310/2 + text_height/2, text_width, 2))