from .constants import ROW, COL

class SimpleBoard:
	
	def __init__(self, board, killed_goats, unused_goats, trapped_tigers):
		self.board = []
		self.killed_goats = killed_goats
		self.unused_goats  = unused_goats
		self.trapped_tigers = trapped_tigers
		self.create_board(board)

	# def draw_circles(self, win):

	# 	win.blit(BOARD, (30, 20))

	# 	for row in range(ROW):
	# 		for col in range(COL):
	# 			circle = Circle(row, col)
	# 			circle.draw(win)



	def create_board(self, board):
		for row in range(ROW):
			self.board.append([])
			for col in range(COL):
				if board[row][col] == 0 or repr(board[row][col]) == "valid":
					self.board[row].append(0)
				else:
					self.board[row].append(repr(board[row][col]))


	def move(self, tuple):
		from_row = tuple[0]
		from_col = tuple[1]
		to_row = tuple[2]
		to_col = tuple[3]

		if from_row == -1:
			self.board[to_row][to_col] = "goat"
			self.unused_goats-=1

		else:
			self.board[from_row][from_col], self.board[to_row][to_col] = self.board[from_row][from_col], self.board[to_row][to_col]
			if self.board[from_row][from_col] == "bagh":
				if (to_row, to_col) not in self._get_common_moves(from_row, from_col):
					goat_row = (to_row + from_row)//2
					goat_col = (to_col + from_col)//2
					self.board[goat_row][goat_col] = 0
					self.killed_goats += 1
		self.check_trapped_tigers()  


	def get_piece(self, row, col):
		return self.board[row][col]


	def _get_goat_moves(self, row, col):
		moves = set()

		all_moves = self._get_common_moves(row, col)

		for move in all_moves:
			if self.board[move[0]][move[1]] == 0:
				moves.add(move)

		return moves


	def _get_bagh_moves(self, row, col):
		all_moves = self._get_common_moves(row, col)
		moves = set()
		valid_goat_moves = set()

		for move in all_moves:
			
			if self.board[move[0]][move[1]] == 0:
				moves.add(move)

			elif self.board[move[0]][move[1]] == "goat":
				valid_goat_moves = self._get_common_moves(move[0], move[1])
				goat_row = move[0]
				goat_col = move[1]
				row_to_add = goat_row + (goat_row - row)
				col_to_add = goat_col + (goat_col - col)

				if (row_to_add, col_to_add) in valid_goat_moves:
					if self.board[row_to_add][col_to_add] == 0:
						moves.add((row_to_add, col_to_add))		
		
		return moves




	def _get_common_moves(self, row, col):
		moves = set()
		adjacent_diretions = {(-1, 0), (0, -1), (1, 0), (0, 1)}
		diagonal_directions = {(1, -1), (-1, 1), (1, 1), (-1, -1)}

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

		
	def _get_unused_goat_moves(self):
		moves = set()
		if self.unused_goats > 0:

			for row in range(ROW):
				for col in range(COL):
					if self.board[row][col] == 0:
						moves.add((row, col))

		return moves


	def check_trapped_tigers(self):
		self.trapped_tigers = 0
		for row in range(ROW):
			for col in range(COL):
				piece = self.board[row][col]
				if piece != 0 and piece == "bagh":
					moves = self._get_bagh_moves(row, col)
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
					moves.append((-1, -1, move[0], move[1]))

			else:
				for row in range(ROW):
					for col in range(COL):
						piece = self.board[row][col]
						if piece == "goat":
							possible_moves = self._get_goat_moves(row, col)

							for move in possible_moves:
								moves.append((row, col, move[0], move[1]))

		elif which_piece == "bagh":
			for row in range(ROW):
					for col in range(COL):
						piece = self.board[row][col]
						if piece == "bagh":
							possible_moves = self._get_bagh_moves(row, col)

							for move in possible_moves:
								moves.append((row, col, move[0], move[1]))


		return moves


	
