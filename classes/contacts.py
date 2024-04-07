import pygame as pyg
pyg.init()

from classes.display import Colors, Fonts
from classes.globals import Globals
from modules.collider import collides_point

class Contacts:
    def __init__(self, contacts=[]):
        self.contacts = []
        for contact in contacts:
            self.contacts += [contact]

    def draw(self, window, box=()):
        """Draws the contacts that this object contains"""
        x, y, width, _ = box
        vertical_offset = 0
        y += 10

        # Display contacts
        for contact in self.contacts:
            name = contact["name"][:16]
            text_width, text_height = Fonts.contact_font.size(name)

            # If mouse is hovered over this contact, indicate that by drawing a rounded rectangle behind the text
            if collides_point(Globals.mouse_position, (x + 2, y + vertical_offset - 2, width - 4, text_height + 4)):
                pyg.draw.rect(window, Colors.gray, (x + 2, y + vertical_offset - 2, width - 4, text_height + 4), border_radius=10)

            # If this is the currently selected contact, indicate that
            if contact == Globals.current_contact["contact_object"]:
                pyg.draw.rect(window, Colors.light_gray, (x + 2, y + vertical_offset - 2, width - 4, text_height + 4), border_radius=10)

            window.blit(Fonts.contact_font.render(name, True, Colors.white), (x + (width - text_width)/2, y + vertical_offset))
            vertical_offset += text_height + 8

    def check_mpress(self, box=()):
        """Checks if any of the contacts were clicked, will return the contact if true"""
        x, y, width, _ = box
        vertical_offset = 0
        y += 10

        for i in range(len(self.contacts)):
            _, text_height = Fonts.contact_font.size(self.contacts[i]["name"])
            # Check the mouse collision
            if collides_point(Globals.mouse_position, (x + 2, y + vertical_offset - 2, width - 4, text_height + 4)):
                return self.contacts[i]

            vertical_offset += text_height + 8