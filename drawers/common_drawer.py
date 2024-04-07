import pygame as pyg
pyg.init()

def draw_text(window, text, font, color, rect, center_h=True, center_v=True):
    x, y, width, height = rect
    text_width, text_height = font.size(text)

    x_pos = x + ((width - text_width) / 2 if center_h else width)
    y_pos = y + ((height - text_height) / 2 if center_v else height)

    window.blit(font.render(text, True, color), (x_pos, y_pos))

def draw_box(window, text, font, text_color, rect_color, rect, center_h=True, center_v=True, radius=0):
    x, y, width, height = rect
    text_width, text_height = font.size(text)

    x_pos = x + ((width - text_width) / 2 if center_h else width)
    y_pos = y + ((height - text_height) / 2 if center_v else height)

    pyg.draw.rect(window, rect_color, (x_pos - 2, y_pos - 2, text_width + 4, text_height + 4), border_radius=radius)
    window.blit(font.render(text, True, text_color), (x_pos, y_pos))