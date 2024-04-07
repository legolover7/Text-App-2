# Import statements
import pygame as pyg
pyg.init()

# Custom modules
from classes.display import Colors, Fonts
from classes.globals import Globals
import modules.chunk_text as chunk_text
from modules.collider import collides_point


def draw(objects, active_object):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT

    VID_BUFFER.fill(Colors.black)

    # Draw titlebar component
    draw_titlebar(VID_BUFFER, WIDTH, HEIGHT)

    # Draw sidebar component
    draw_sidebar(VID_BUFFER, HEIGHT)

    # Draw messages component, if any exist
    if Globals.current_contact != {}:
        draw_messages(VID_BUFFER, HEIGHT, objects)

    # Draw typing box component
    objects[0].draw(active_object)
    
    # Draw the current popup component
    draw_popup(VID_BUFFER, WIDTH, HEIGHT, objects, active_object)

def draw_popup(window, WIDTH, HEIGHT, objects, active_object):
    if Globals.current_menu == "Add contact":
        new_contact_username = objects[1]
        new_contact_email = objects[2]

        # Draw background
        pyg.draw.rect(window, Colors.gray, (1200, 200, 400, HEIGHT-400), border_radius=10)
        pyg.draw.rect(window, Colors.dark_gray, (1202, 202, 396, HEIGHT-404), border_radius=10)
        
        # Draw text
        text_width = Fonts.new_contact.size("Create New Contact")[0]
        window.blit(Fonts.new_contact.render("Create New Contact", True, Colors.white), (1200 + (400 - text_width)/2, 210))
        
        # Draw input fields
        new_contact_username.draw(active_object)
        new_contact_email.draw(active_object)

def draw_titlebar(window, WIDTH, HEIGHT):
    """Draws the titlebar containing the close/settings icons"""
    # Settings button icon
    if collides_point(Globals.mouse_position, circle=(WIDTH-60, 24, 14)):
        pyg.draw.circle(window, Colors.gray, (WIDTH-60, 24), 14)
    window.blit(pyg.image.load("assets/settings.png"), (WIDTH-75, 9))

    # Close button icon
    if collides_point(Globals.mouse_position, circle=(WIDTH-25, 24, 14)):
        pyg.draw.circle(window, Colors.gray, (WIDTH-25, 24), 14)
    window.blit(pyg.image.load("assets/close.png"), (WIDTH-40, 10))


def draw_sidebar(window, HEIGHT):
    """Draws the sidebar containing the list of contacts"""
    pyg.draw.rect(window, Colors.dark_gray, (5, 5, 200, HEIGHT-10), border_radius=5)
    Globals.contacts.draw(window, (5, 40, 200, HEIGHT-45))

    # Draw "Add new contact" button
    color = Colors.light_gray if collides_point(Globals.mouse_position, (10, 10, 190, 25)) else Colors.gray
    pyg.draw.rect(window, color, (10, 10, 190, 25), border_radius=10)
    text_width, text_height = Fonts.contact_font.size("Add new contact")
    window.blit(Fonts.contact_font.render("Add new contact", True, Colors.white), (10 + (190 - text_width)/2, 10 + (25 - text_height)/2))

def draw_messages(window, HEIGHT, objects):
    """Draws the messages of the current contact"""
    contact = Globals.current_contact["account_name"]
    last_message = ""
    
    # Shift message upwards based on how large the message box currently is
    message_box = objects[0]
    message_box_lines = chunk_text.chunk(message_box.text, content_width=message_box.width-5, char_width=message_box.font.size("A")[0])
    offset = max(0, (len(message_box_lines) - 1) * (message_box.font.size("A")[1] + 2))
  
    vertical_offset = HEIGHT - 130 - offset

    for message in Globals.messages[contact]:
        # Display messages
        if ("message") in message:
            text_list = [""]
            if len(message["message"].strip()) > 0:
                text_list = chunk_text.chunk(message["message"], 60)
            text_width = 0
            for t in text_list:
                size, x = Fonts.text_font.size(t)
                if size > text_width:
                    text_width = size

            # User's messages
            if message["from"] != contact:
                if last_message == contact or last_message == "":
                    vertical_offset -= 4
                else:
                    vertical_offset -= 14
                
                pyg.draw.rect(window, Colors.green, (996-text_width, vertical_offset - 2 - 18*(len(text_list)-1), text_width+8, 20 + 18*(len(text_list)-1)), 0, 8)

                for line in reversed(text_list):
                    window.blit(Fonts.text_font.render(line, True, Colors.white), (1000-text_width, vertical_offset))
                    vertical_offset -= 18
                last_message = contact

            # Contact's messages
            else:
                if last_message != contact or last_message == "":
                    vertical_offset -= 4
                else:
                    vertical_offset -= 14
                pyg.draw.rect(window, Colors.gray, (296, vertical_offset - 2 - 18*(len(text_list)-1), text_width+8, 20 + 18*(len(text_list)-1)), 0, 8)

                for line in reversed(text_list):
                    window.blit(Fonts.text_font.render(line, True, Colors.white), (300, vertical_offset))
                    vertical_offset -= 18
                last_message = "no"
