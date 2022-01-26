from .board import Board
from .piece import Goat
from .constants import GOAT
from .circle import Circle
from .constants import CRIMSON, BOARD, BAGH, GOAT, ROW, COL


class Game:

	def __init__(self, win, ai):
		self.win = win
		self._init(ai)


	def _init(self, ai):
		self.selected = None
		self.board = Board()
		self.turn = "goat"
		self.ai = ai
		self.winner = None
		self.valid_moves = set()
		self.draw()

	def select(self, row, col):

		self.board.remove_valid_moves()
		self.draw()

		if self.turn == "goat" and self.board.unused_goats > 0:
			if repr(self.board.get_piece(row, col)) != "bagh":
				piece = Goat(row, col, GOAT)
				self.selected = piece
				self.valid_moves = self.board.get_valid_moves()
				self._move(row, col)

		else:
 
			if self.selected:
				result = self._move(row, col)
				if not result:
					self.selected = None
					self.select(row, col)
			else:
				piece =  self.board.get_piece(row, col)
				if piece != 0 and repr(piece) == self.turn:
					self.selected = piece
					self.valid_moves = self.board.get_valid_moves(piece)
					self.board.show_valid_moves(self.valid_moves)
					self.draw()
					return True			


	def change_turn(self):
		if self.turn == "goat":
			self.turn = "bagh"
		else:
			self.turn = "goat"

		self.board.remove_valid_moves()
		self.draw()


	def _move(self, row, col):

		
		piece = self.board.get_piece(row, col)
		if self.selected and (piece == 0 or repr(piece) == "valid") and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			self.board.remove_valid_moves()
			self.draw()
			self.change_turn()
		else:
			return False

		return True

	def show_goat_moves(self):
		self.valid_moves = self.board.get_valid_moves()
		self.board.show_valid_moves(self.valid_moves)
		self.draw()

	def draw(self):
		self.draw_circles(self.win)
		self.board.draw(self.win)

	def draw_circles(self, win):

		win.blit(BOARD, (30, 20))

		for row in range(ROW):
			for col in range(COL):
				circle = Circle(row, col)
				circle.draw(win)


	

