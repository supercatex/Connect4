#!usr/bin/env python

from GameBoard import *
from Agent import *
import time


if __name__ == "__main__":
	p1 = 0
	p2 = 0
	is_print = False
	for i in range(100):
		g = GameBoard()
		if is_print:
			g.print_board()

		players = [UCTAgent("COM1", 1, g), NStepAgent("COM2", 2, g, 10)]
		
		while len(g.get_choices()) > 0:
			p = players[g.player - 1]
			c = p.get_choice()
			g.move(c, g.player)
			if is_print:
				g.print_board()
			if g.is_winner(c, g.player):
				print(p.name + " is WINNER!")
				if p.player == 1:
					p1 += 1
				if p.player == 2:	
					p2 += 1
				break
			g.next_player()
			# time.sleep(1)
		print("%.4f, %.4f, %.4f, %d" % (p1 / (i + 1), p2 / (i + 1), (i + 1 - p1 - p2) / (i + 1), i + 1))

