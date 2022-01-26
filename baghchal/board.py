from .constants import CRIMSON, BOARD, BAGH, GOAT, ROW, COL
import pygame as pg
from .piece import Bagh, Goat
from .circle import Circle
from .circle import GreenCircle


class Board:
	
	def __init__(self):
		self.board = []
		self.killed_goats = 0
		self.unused_goats  = 20
		self.trapped_tigers = 0
		self.create_board()

	# def draw_circles(self, win):

	# 	win.blit(BOARD, (30, 20))

	# 	for row in range(ROW):
	# 		for col in range(COL):
	# 			circle = Circle(row, col)
	# 			circle.draw(win)



	def create_board(self):
		for row in range(ROW):
			self.board.append([])
			for col in range(COL):
				if row == 0 or row == ROW - 1:
					if col == 0 or col == COL - 1:
						self.board[row].append(Bagh(row, col, BAGH))
					else:
						self.board[row].append(0)
				else:
					self.board[row].append(0)


	def draw(self, win):
		for row in range(ROW):
			for col in range(COL):
				piece = self.board[row][col]
				if piece != 0:
					piece.draw(win)


	def move(self, piece, row, col):
		if piece.row == row and piece.col == col:
			self.board[row][col] = piece
			self.unused_goats -= 1

		else:
			self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
			if repr(piece) == "bagh":
				if (row, col) not in self._get_common_moves(piece):
					goat_row = (row + piece.row)//2
					goat_col = (col + piece.col)//2
					self.board[goat_row][goat_col] = 0
					self.killed_goats += 1
			piece.move(row, col)
		self.check_trapped_tigers()  


	def get_piece(self, row, col):
		return self.board[row][col]


	def get_valid_moves(self, piece=None):
		moves = set()
		if piece == None:
			return self._get_unused_goat_moves()
		else:
			if repr(piece) == "goat":
				moves = self._get_goat_moves(piece);
			else:
				moves = self._get_bagh_moves(piece)
		
		return moves

	def _get_goat_moves(self, piece):
		moves = set()

		all_moves = self._get_common_moves(piece)

		for move in all_moves:
			if self.board[move[0]][move[1]] == 0:
				moves.add(move)

		return moves


	def _get_bagh_moves(self, piece):
		all_moves = self._get_common_moves(piece)
		moves = set()
		valid_goat_moves = set()

		for move in all_moves:
			
			if self.board[move[0]][move[1]] == 0 or repr(self.board[move[0]][move[1]]) == "valid":
				moves.add(move)

			elif repr(self.board[move[0]][move[1]]) == "goat":
				valid_goat_moves = self._get_common_moves(self.board[move[0]][move[1]])
				goat_row = move[0]
				goat_col = move[1]
				row_to_add = goat_row + (goat_row - piece.row)
				col_to_add = goat_col + (goat_col - piece.col)

				if (row_to_add, col_to_add) in valid_goat_moves:
					if self.board[row_to_add][col_to_add] == 0 or repr(self.board[row_to_add][col_to_add]) == "valid":
						moves.add((row_to_add, col_to_add))		
		
		return moves




	def _get_common_moves(self, piece):
		moves = set()
		adjacent_diretions = {(-1, 0), (0, -1), (1, 0), (0, 1)}
		diagonal_directions = {(1, -1), (-1, 1), (1, 1), (-1, -1)}
		row, col = piece.row, piece.col

		for coords in adjacent_diretions:
			row_to_add = row + coords[0]
			col_to_add = col + coords[1]

			if row_to_add >= 0 and row_to_add < ROW and col_to_add >= 0 and col_to_add < COL:
				moves.add((row+coords[0], col+coords[1]))								

		if (row + col)%2 == 0:
			for coords in diagonal_directions:
				row_to_add = row + coords[0]
				col_to_add = col + coords[1]

				if row_to_add >= 0 and row_to_add < ROW and col_to_add >= 0 and col_to_add < COL:
					moves.add((row+coords[0], col+coords[1]))

		return moves


	def show_valid_moves(self, valid_moves):
		for row_col in valid_moves:
			row = row_col[0]
			col = row_col[1]

			self.board[row][col] = GreenCircle(row, col)


	def remove_valid_moves(self):
		for row in range(ROW):
			for col in range(COL):
				if self.board[row][col] != 0 and repr(self.board[row][col]) == "valid":
					self.board[row][col] = 0
 


		
	def _get_unused_goat_moves(self):
		moves = set()
		if self.unused_goats > 0:

			for row in range(ROW):
				for col in range(COL):
					if self.board[row][col] == 0:
						moves.add((row, col))

		return moves

	def add_goat_to_board(self, row, col):
		piece = Goat(row, col, GOAT)
		self.board[row][col] = piece
		self.check_trapped_tigers()
		self.unused_goats -= 1


	def check_trapped_tigers(self):
		self.trapped_tigers = 0
		for row in self.board:
			for piece in row:
				if piece != 0 and repr(piece) == "bagh":
					moves = self._get_bagh_moves(piece)
					if len(moves) == 0:
						self.trapped_tigers += 1


	def get_winner(self):
		if self.trapped_tigers >= 4:
			return "goat"

		if self.killed_goats >= 5:
			return "bagh"


	def is_game_over(self):
		if self.trapped_tigers >= 4 or self.killed_goats >= 5:
			return True

		return False


	def generate_moves_for_all_pieces(self, which_piece):
		moves = list()

		if which_piece == "goat":

			if self.unused_goats > 0:
				possible_moves = self._get_unused_goat_moves()

				for move in possible_moves:
					goat_piece = Goat(move[0], move[1], GOAT)
					moves.append((goat_piece, move[0], move[1]))

			else:
				for row in ROW:
					for col in COL:
						piece = self.get_piece(row, col)
						if repr(piece) == "goat":
							possible_moves = self._get_goat_moves(piece)

							for move in possible_moves:
								moves.append(piece, move[0], move[1])

		elif which_piece == "bagh":
			for row in ROW:
					for col in COL:
						piece = self.get_piece(row, col)
						if repr(piece) == "goat":
							possible_moves = self._get_bagh_moves(piece)

							for move in possible_moves:
								moves.append(piece, move[0], move[1])


		return moves


	
