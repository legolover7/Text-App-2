import pygame as pyg
pyg.init()

class Globals:
    # Default size of the application
    WIDTH, HEIGHT = (1920, 1080)
    # User's monitor size
    WINDOW_WIDTH, WINDOW_HEIGHT = (1920, 1080)
    # Actual window object that gets displayed to the user
    WINDOW = None
    # Image buffer that gets scaled to the user's monitor size, from the default size
    VID_BUFFER = pyg.surface.Surface((WIDTH, HEIGHT))

    # Max FPS of application
    FPS = 60
    # Pygame clock object for controlling the framerate
    clock = pyg.time.Clock()

    # Current position of mouse cursor
    mouse_position = (0, 0)

    # Currently selected contact
    current_contact = {}
    # User's messages
    messages = {}
    contacts = None
    current_message = ""
    cursor_position = 0
    username = ""
    contact_list = []
    contact_account_names = []
    current_menu = ""