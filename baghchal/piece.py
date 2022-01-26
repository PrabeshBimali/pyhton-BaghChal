from .constants import PIECE_ROW, PIECE_COL, DIFFERENCE

class Piece:

	def __init__(self, row, col, piece_type):
		self.row = row
		self.col = col
		self.x = 0
		self.y = 0
		self.image = piece_type
		self.rect = self.image.get_rect()
		self.calc_pos()

	def calc_pos(self):
		self.x = PIECE_ROW + (DIFFERENCE * self.row)
		self.y = PIECE_COL + (DIFFERENCE * self.col)
		self.rect.top = self.x
		self.rect.left = self.y


	def draw(self, win):
		win.blit(self.image, self.rect)


	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()




class Bagh(Piece):

	def __init__(self, row, col, piece_type):
		Piece.__init__(self, row, col, piece_type)


	def __repr__(self):
		return "bagh"


class Goat(Piece):
	def __init__(self, row, col, piece_type):
		Piece.__init__(self, row, col, piece_type)


	def __repr__(self):
		return "goat"
