import pygame as pyg
pyg.init()
import sys

from classes.display import Fonts
from classes.globals import Globals
from classes.contacts import Contacts
from drawers.texting_drawer import draw
from env import ENV
from classes.input_field import InputField
from modules.collider import collides_point
import database.database as database
import modules.typing_handler as typing_handler

def Texting():
    Globals.contacts = Contacts(Globals.contact_list)
    # There's a difference between the username that the current user has set for a given account, vs the actual account name
    Globals.contact_account_names = []
    # Various input fields
    message_box = InputField((346, 1000, 658, 22), Fonts.contact_font, "Enter message")
    new_contact_username = InputField((1205, 300, 300, 30), Fonts.contact_font, "Enter contact's username")
    objects = [message_box, new_contact_username]
    active_object = message_box


    try:
        # Load user's messages
        for contact in Globals.contacts.contacts:
            # Get the contact's address
            address = contact["address"]
            # Search for actual username 
            contact_object = database.query("accounts", query={"email": address})
            for co in contact_object:
                contact_name = co["username"]
                Globals.contact_account_names += [contact_name]

            # Get messages between the two users
            Globals.messages[contact_name] = []
            m = database.query("messages", query={"from": { "$in": [contact_name, Globals.username]}, "to": { "$in": [contact_name, Globals.username]}}, limit=50)
            for message in m:
                Globals.messages[contact_name] += [message]

            # Reverse the list so the latest messages are shown first
            Globals.messages[contact_name].reverse()
        Globals.current_contact = {"contact_object": Globals.contacts.contacts[0], "account_name": Globals.contact_account_names[0]}
    except IndexError:
        # User doesn't have any saved contacts
        pass

    while True:
        # Get mouse position
        Globals.mouse_position = pyg.mouse.get_pos()

        # Get events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            # User pressed a keyboard button
            elif event.type == pyg.KEYDOWN:
                # Get the pressed key and any current keyboard mods
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                # Kill key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

                # Return to login key
                elif key == pyg.K_F2:
                    return "Login"

                # Send message (so long as it's not empty)
                elif key == pyg.K_RETURN and Globals.current_message != "" and active_object == None:
                    # Add message to database and user's messages
                    to = Globals.current_contact["account_name"]
                    database.insert("messages", {"from": Globals.username, "to": to, "message": Globals.current_message})
                    Globals.messages[to].insert(0, {"from": Globals.username, "to": to, "message": Globals.current_message})
                    # Reset message and cursor position
                    Globals.current_message = ""
                    Globals.cursor_position = 0

                # Ctrl+Tab cycling through contacts
                elif ctrl and key == pyg.K_TAB:
                    index = Globals.contacts.contacts.index(Globals.current_contact["contact_object"])
                    index += -1 if shift else 1
                    if index == len(Globals.contacts.contacts):
                        index = 0

                    try:
                        Globals.current_contact = {"contact_object": Globals.contacts.contacts[index], "account_name": Globals.contact_account_names[index]}
                    except IndexError:
                        print("Invalid contact")
                    
                else:
                    active_object.text, Globals.cursor_position = typing_handler.handler(active_object.text, key, (shift, caps, ctrl), Globals.cursor_position)

            # LMB press
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the message box was clicked
                if message_box.check_mcollision():
                    active_object = message_box
                    Globals.cursor_position = len(active_object.text)
                
                # Check if the add new contact button was clicked
                if collides_point(Globals.mouse_position, (10, 10, 190, 25)):
                    Globals.current_menu = "Add contact"

                # Check if one of the contacts were clicked
                contact = Globals.contacts.check_mpress((5, 40, 200, Globals.HEIGHT - 10))
                if contact is not None:
                    # Get the index of the contact that was clicked, and update the current contact
                    index = Globals.contacts.contacts.index(contact)
                    try:
                        Globals.current_contact = {"contact_object": Globals.contacts.contacts[index], "account_name": Globals.contact_account_names[index]}
                    except IndexError:
                        print("Invalid contact")

                if Globals.current_menu == "Add contact":
                    # Check if the new contact fields were clicked
                    if new_contact_username.check_mcollision():
                        active_object = new_contact_username
                        Globals.cursor_position = len(active_object.text)
        
        # Refresh display
        draw(objects, active_object)
        
        # Transform 1920x1080 image buffer to user's screen size
        Globals.WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
        pyg.display.update()

        Globals.clock.tick(Globals.FPS)