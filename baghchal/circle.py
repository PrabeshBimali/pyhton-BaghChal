from .constants import LIGHT_BLUE, LIGHT_GREEN, CIRCLE_ROW, CIRCLE_COL, DIFFERENCE

import pygame as pg

class Circle:

	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.radius = 35
		self.x = 0
		self.y = 0
		self.calculate_pos()

	def calculate_pos(self):

		# x value is calculated using cloumn because both grew in horizontal ===> direction

		self.x = CIRCLE_COL + (self.col * DIFFERENCE)
		self.y = CIRCLE_ROW + (self.row * DIFFERENCE)

	def draw(self, win):
		pg.draw.circle(win, LIGHT_BLUE, (self.x, self.y), 30)

	def get_radius(self):
		return self.radius

	def get_distance_from_center(self, x, y):
		val = ((x-self.x)**2) + ((y-self.y)**2)

		return val**(1/2)


class GreenCircle(Circle):
	def __init__(self, row, col):
		Circle.__init__(self, row, col)

	def draw(self, win):
		pg.draw.circle(win, LIGHT_GREEN, (self.x, self.y), 30)

	def __repr__(self):
		return "valid"
