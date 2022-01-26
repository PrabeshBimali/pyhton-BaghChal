import pygame as pg

CRIMSON = (102, 7, 8);
GREY = (22, 26, 29);
LIGHT_BLUE = (70, 143, 175);
LIGHT_GREEN = (60, 179, 113);

ROW = 5
COL = 5


WIDTH = 1000;
HEIGHT = 700;

BOARD = pg.transform.scale(pg.image.load('baghchal/assets/board.png'), (650, 650))

BAGH = pg.image.load('baghchal/assets/bagh.png')
GOAT = pg.image.load('baghchal/assets/goat.png')

PIECE_ROW = 27.5
PIECE_COL = 36.5

CIRCLE_ROW = 59
CIRCLE_COL = 68
DIFFERENCE = 144
