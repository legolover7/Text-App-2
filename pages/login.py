# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()
import json
import sys
import os

# Custom modules
from classes.display import Colors, Fonts
from classes.globals import Globals
from drawers.login_drawer import draw
from classes.input_field import InputField
from classes.buttons import Button, Dropdown
import modules.typing_handler as typing_handler
import database.database as database
from modules.collider import collides_point

def Login():
    # Input fields
    email_field = InputField((Globals.WIDTH/2-200, 450, 400, 30), Fonts.contact_font, "Enter email")
    password_field = InputField((Globals.WIDTH/2-200, 500, 400, 30), Fonts.contact_font, "Enter password")
    
    # Buttons
    login_button = Button((Globals.WIDTH/2-100, 550, 200, 60), Colors.blue, "Login", Fonts.login_header_2, Colors.white)
    settings_button = Button((Globals.WIDTH/2-120, 700, 240, 45), Colors.gray, "Settings", Fonts.login_header_2, Colors.white)
    quit_button = Button((Globals.WIDTH/2-80, 760, 160, 45), Colors.gray, "Quit", Fonts.login_header_2, Colors.white)
    account_dropdown = Dropdown((Globals.WIDTH-200, 5, 195, 30), Fonts.contact_font, Colors.dark_gray, [""], Colors.white)

    active_field = None
    saved_accounts = {}
    error_message = ""

    try:
        with open("data/saved_accounts.json", "r") as file:
            saved_accounts = json.load(file)
            if len(saved_accounts["accounts"]):
                email_field.text = saved_accounts["accounts"][0]["email"]
                password_field.text = saved_accounts["accounts"][0]["password"]

                # Setup the saved account dropdown
                account_dropdown.options = []
                for account in saved_accounts["accounts"]:
                    # Account selection dropdown
                    account_dropdown.options += [account["username"]]
                account_dropdown.selected = account_dropdown.options[0]

    except FileNotFoundError:
        try:
            os.mkdir("data")
        except FileExistsError:
            pass
        with open("data/saved_accounts.json", "w") as file:
            file.write(json.dumps({"accounts": []}, indent=4))

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
                    elif active_field == password_field:
                        active_field = None
                    else:
                        active_field = email_field

                # Enter key 
                elif key == pyg.K_RETURN:
                    # If the active field is the email one, set the password as the active field, otherwise submit form
                    if active_field == email_field:
                        active_field = password_field
                    else:
                        # Check the credentials of the two fields
                        return_value = verify_account(email_field.text, password_field.text, saved_accounts)
                        if return_value in ["Invalid Password", "Account not Found"]:
                            # Password was invalid or the account doesn't exist
                            password_field.text = ""
                            active_field = None
                            error_message = return_value
                        else:
                            return "Texting"
                else:
                    # If one of the fields are active, update its text content
                    if active_field is not None:
                        active_field.text, Globals.cursor_position = typing_handler.handler(active_field.text, key, (shift, caps, ctrl), Globals.cursor_position)

                
            # Mouse button pressed
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                active_field = None
                # Check if the register link was clicked
                text_width, text_height = Fonts.contact_font.size("Sign Up")
                if collides_point(Globals.mouse_position, ((Globals.WIDTH + 280 - text_width)/2, 1310/2 - text_height/2, text_width, text_height)):
                    return "Register"
                
                # Check if the login button was clicked
                if login_button.check_mcollision():
                    # Check the credentials of the two fields
                    return_value = verify_account(email_field.text, password_field.text, saved_accounts)
                    if return_value in ["Invalid Password", "Account not Found"]:
                        # Password was invalid or the account doesn't exist
                        password_field.text = ""
                        active_field = None
                        error_message = return_value
                    else:
                        return "Texting"

                # Check if the settings/quit buttons were clicked
                elif settings_button.check_mcollision():
                    pass
                elif quit_button.check_mcollision():
                    pyg.quit()
                    sys.exit()


                # Check if the two different input fields were clicked, set the respective one as active if so
                elif email_field.check_mcollision():
                    active_field = email_field
                    Globals.cursor_position = len(active_field.text)
                elif password_field.check_mcollision():
                    active_field = password_field
                    Globals.cursor_position = len(active_field.text)

                # Check if the account dropdown was clicked
                username = account_dropdown.click()
                if username != "" and username is not None:
                    for account in saved_accounts["accounts"]:
                        # Set the email, password, and current contacts equal to the saved object's data
                        if account["username"] == username:
                            email_field.text = account["email"]
                            password_field.text = account["password"]
                            Globals.contact_list = account["contacts"]

        # Refresh screen
        draw(error_message)
        # Draw the different objects of the page
        email_field.draw(active_field)
        password_field.draw(active_field)
        login_button.draw()
        settings_button.draw()
        quit_button.draw()
        account_dropdown.draw()

        # Transform 1920x1080 image buffer to user's screen size
        Globals.WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
        pyg.display.update()

        Globals.clock.tick(Globals.FPS)

def verify_account(email, password, saved_accounts):
    """Searches the database for a account with the given email and password"""
    accs = database.query("accounts", query={"email": email})
    for acc in accs:
        if acc["password"] == password:
            # Re/set data
            Globals.username = acc["username"]
            Globals.contact_list = []
            Globals.contact_account_names = []
            Globals.messages = {}
            Globals.current_contact = {}

            # Get account's saved contacts
            for account in saved_accounts["accounts"]:
                if account["username"] == Globals.username:
                    Globals.contact_list = account["contacts"]
            return acc["username"]
        else:
            return "Invalid Password"
        
    return "Account not Found"
            