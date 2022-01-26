import sys
import time
import pygame as pg;
from baghchal.constants import CRIMSON, GREY, WIDTH, HEIGHT;
from baghchal.board import Board;
from baghchal.game import Game;
from display_text import show_text, show_btn
from baghchal.minimax import Ai


INF = 10e6
FPS = 60

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("BaghChal")



def main():

	ai = "bagh"

	if len(sys.argv) > 1:
		if sys.argv[1] == "goat" or sys.argv[1] == "bagh":
			ai = sys.argv[1]



	run = True
	game_instance = Game(screen, ai)
	clock = pg.time.Clock()

	while run:
		clock.tick(FPS)

		for event in pg.event.get():

			screen.fill(GREY)


			if event.type == pg.QUIT:
				run = False;


			

			

			if game_instance.turn == "goat" and game_instance.board.unused_goats > 0:
				game_instance.show_goat_moves()				
		

			if game_instance.turn == game_instance.ai:
				ai = Ai()
				best_move = ai.get_best_move(game_instance.board, game_instance.ai)[0]
				if game_instance.ai == "goat":
					if game_instance.board.unused_goats > 0:
						time.sleep(2)
						game_instance.select(best_move[2], best_move[3])
					else:
						game_instance.select(best_move[0], best_move[1])
						time.sleep(3)
						game_instance.select(best_move[2], best_move[3])

				elif game_instance.ai == "bagh":
					game_instance.select(best_move[0], best_move[1])
					time.sleep(3)
					game_instance.select(best_move[2], best_move[3])
			else:
				if event.type == pg.MOUSEBUTTONDOWN:
					x, y = event.pos
					send_row_and_col(x, y, game_instance)

			if game_instance.board.is_game_over():
				if game_instance.board.get_winner() == "bagh":
					game_over_screen(clock, screen, "Bagh", game_instance)

				else:
					game_over_screen(clock, screen, "Goat", game_instance)

				game_instance = Game(screen, game_instance.ai)


			show_text(screen, "Turn", game_instance.turn, 850, 250)
			show_text(screen, "Goats killed", str(game_instance.board.killed_goats), 850, 300)
			show_text(screen, "Tigers trapped", str(game_instance.board.trapped_tigers), 850, 350)
			show_text(screen, "unused goats", str(game_instance.board.unused_goats), 850, 400)			
					


			game_instance.draw()
			pg.display.update()

			



def send_row_and_col(x, y, game_instance):


	for row in game_instance.board.board:
		for piece in row:
			if piece != 0:
				if repr(piece) != "valid":
					if piece.rect.collidepoint(x, y):
						game_instance.select(piece.row, piece.col)
				else:
					if piece.get_distance_from_center(x, y) < piece.get_radius():
						game_instance.select(piece.row, piece.col)





def game_over_screen(clock, screen, winner, game_instance):
	waiting = True
	while waiting:
		
		clock.tick(FPS)

		for event in pg.event.get():	

			show_text(screen, "Goats killed", str(game_instance.board.killed_goats), 850, 300)
			show_text(screen, "Tigers trapped", str(game_instance.board.trapped_tigers), 850, 350)
			show_text(screen, "Winner", winner, 850, 400)
			restart_btn = show_btn(screen, "Restart", 850, 450)

			game_instance.draw()

			if event.type == pg.MOUSEBUTTONDOWN:
				x, y = event.pos

				if restart_btn.collidepoint(x, y):
					waiting = False

			if event.type == pg.QUIT:
				sys.exit("Game Quit")

		pg.display.update()


if __name__ == '__main__':
	main();