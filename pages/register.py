# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()
import json
import sys
import re

# Custom modules
from classes.display import Colors, Fonts
from classes.globals import Globals
from drawers.register_drawer import draw
from classes.input_field import InputField
from classes.buttons import Button, Dropdown
import modules.typing_handler as typing_handler
import database.database as database
from modules.collider import collides_point

def Register():
    # Input fields
    username_field = InputField((Globals.WIDTH/2-200, 350, 400, 30), Fonts.contact_font, "Enter username")
    email_field = InputField((Globals.WIDTH/2-200, 400, 400, 30), Fonts.contact_font, "Enter email")
    password_field = InputField((Globals.WIDTH/2-200, 450, 400, 30), Fonts.contact_font, "Enter password")
    confirm_password_field = InputField((Globals.WIDTH/2-200, 500, 400, 30), Fonts.contact_font, "Confirm password")
    
    # Buttons
    register_button = Button((Globals.WIDTH/2-100, 550, 240, 60), Colors.blue, "Register", Fonts.login_header_2, Colors.white)
    settings_button = Button((Globals.WIDTH/2-120, 700, 240, 45), Colors.gray, "Settings", Fonts.login_header_2, Colors.white)
    quit_button = Button((Globals.WIDTH/2-80, 760, 160, 45), Colors.gray, "Quit", Fonts.login_header_2, Colors.white)

    active_field = None
    error_message = ""

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
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                # Kill key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()
                
                # Tab key
                elif key == pyg.K_TAB:
                    if active_field == email_field:
                        active_field = password_field
                        Globals.cursor_position = len(active_field.text)
                    elif active_field == password_field:
                        active_field = confirm_password_field
                        Globals.cursor_position = len(active_field.text)
                    elif active_field == confirm_password_field:
                        active_field = None
                    else:
                        active_field = email_field
                        Globals.cursor_position = len(active_field.text)

                # Enter key 
                elif key == pyg.K_RETURN:
                    # Cycle through fields, or submit form if the confirm passsword field is selected
                    if active_field == username_field:
                        active_field = email_field
                    elif active_field == email_field:
                        active_field = password_field
                    elif active_field == password_field:
                        active_field = confirm_password_field
                    else:
                        pass
                    if active_field is not None:
                        Globals.cursor_position = len(active_field.text)
                else:
                    # If one of the fields are active, update its text content
                    if active_field is not None:
                        active_field.text, Globals.cursor_position = typing_handler.handler(active_field.text, key, (shift, caps, ctrl), Globals.cursor_position)
                
            # Mouse button pressed
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                active_field = None
                
                # Check if the login link was clicked
                text_width, text_height = Fonts.contact_font.size("Login")
                if collides_point(Globals.mouse_position, ((Globals.WIDTH + 330 - text_width)/2, 1310/2 - text_height/2, text_width, text_height)):
                    return "Login"

                # Check if the login button was clicked
                if register_button.check_mcollision():
                    return_value = register_account(username_field.text, email_field.text, password_field.text, confirm_password_field.text)
                    if return_value in ["Passwords do not match", "Invalid email", "Please enter a username", "Please enter an email address", "Please enter a password"]:
                        # Password was invalid or the account doesn't exist
                        if return_value != "Passwords don't match":
                            password_field.text = ""
                        confirm_password_field.text = ""
                        active_field = None
                        error_message = return_value
                    else:
                        Globals.username = return_value
                        return "Texting"

                # Check if the settings/quit buttons were clicked
                elif settings_button.check_mcollision():
                    pass
                elif quit_button.check_mcollision():
                    pyg.quit()
                    sys.exit()


                # Check if the two different input fields were clicked, set the respective one as active if so
                elif username_field.check_mcollision():
                    active_field = username_field
                elif email_field.check_mcollision():
                    active_field = email_field
                elif password_field.check_mcollision():
                    active_field = password_field
                elif confirm_password_field.check_mcollision():
                    active_field = confirm_password_field

                if active_field is not None:
                    Globals.cursor_position = len(active_field.text)

        # Refresh screen
        draw(error_message)
        # Draw the different objects of the page
        username_field.draw(active_field)
        email_field.draw(active_field)
        password_field.draw(active_field)
        confirm_password_field.draw(active_field)
        register_button.draw()
        settings_button.draw()
        quit_button.draw()

        # Transform 1920x1080 image buffer to user's screen size
        Globals.WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
        pyg.display.update()

        Globals.clock.tick(Globals.FPS)

def register_account(username, email, password, conf_password):
    if username == "":
        return "Please enter a username"
    elif email == "":
        return "Please enter an email"
    elif password == "":
        return "Please enter a password"
    
    elif password != conf_password:
        return "Passwords do not match"
    
    accs = database.query("accounts", query={"email": email})
    for acc in accs:
        return "Account already exists"

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        database.insert("accounts", {
            "username": username,
            "email": email,
            "password": password
        })

        # Add account to the list of saved accounts
        with open("data/saved_accounts.json", "rw") as file:
            data = json.load(file)
            data["accounts"] += [{
                "username": username,
                "email": email,
                "password": password
            }]
            file.write(json.dump(data))
        Globals.contact_list = []
        return username
    return "Invalid email"
