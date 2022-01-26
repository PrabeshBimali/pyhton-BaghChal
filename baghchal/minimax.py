from copy import deepcopy
from .simple_board import SimpleBoard
INF = 1e6


class Ai:

    def __init__(self, depth=5):
        self.depth = depth

    def static_evaluation(self, board):
        end = board.is_game_over()
        if not end:
            return 1.5 * board.trapped_tigers - 1.2 * board.killed_goats
        winner = board.get_winner()
        if winner == "goat":
            return INF
        elif winner == "bagh":
            return -INF
        else:
            return 0

    def minimax(self, board, depth=0, alpha=-INF, beta=INF, maxPlayer=True):
        if depth == 0 or board.is_game_over():
            return 0, self.static_evaluation(board)

        if maxPlayer:
            maxEval = -INF*10
            best_move = 0
            for move in board.generate_moves_for_all_pieces("goat"):
                b_copy = deepcopy(board)
                b_copy.move(move)
                eval_ = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if eval_ > maxEval:
                    maxEval = eval_
                    best_move = move
                alpha = max(alpha, eval_)
                if beta <= alpha:
                    break
            return best_move, maxEval
        else:
            minEval = INF*10
            best_move = 0
            
            for move in board.generate_moves_for_all_pieces("bagh"):
                b_copy = deepcopy(board)
                b_copy.move(move)
                eval_ = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if eval_ < minEval:
                    minEval = eval_
                    best_move = move
                beta = min(beta, eval_)
                if beta <= alpha:
                    break
            return best_move, minEval

    def _best_bagh_move(self, board):
        assert not board.is_game_over()
        return self.minimax(board, self.depth, maxPlayer=False)

    def _best_goat_move(self, board):
        assert not board.is_game_over()
        return self.minimax(board, self.depth, maxPlayer=True)

    def get_best_move(self, board, turn):
        board = SimpleBoard(board.board, board.killed_goats, board.unused_goats, board.trapped_tigers)
        if turn == "bagh":
            result = self._best_bagh_move(board)
        else:
            result = self._best_goat_move(board)
        return result