import pygame as pg

green = (0, 255, 0)
blue = (0, 0, 128)

def show_text(win, first_text, second_text, width, height):
	pg.init()
	text_string = first_text+ ": "+ second_text
	font = pg.font.Font('freesansbold.ttf', 32)
	text = font.render(text_string, True, green)
	textRect = text.get_rect()
	textRect.center = (width, height)
	win.blit(text, textRect)


def show_btn(win, text_string, width, height):
	pg.init()
	font = pg.font.Font('freesansbold.ttf', 28)
	text = font.render(text_string, True, green, blue)
	textRect = text.get_rect()
	textRect.center = (width, height)
	win.blit(text, textRect)
	return textRect