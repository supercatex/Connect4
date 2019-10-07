#!usr/bin/env python

from GameBoard import *
from Agent import *
import time


if __name__ == "__main__":
	p1 = 0
	p2 = 0
	is_print = True
	for i in range(1):
		g = GameBoard()
		if is_print:
			g.print_board()

		players = [NStepAgent("COM1", 1, g, 12), UCTAgent("COM2", 2, g, 15000)]
		
		while len(g.get_choices()) > 0:
			p = players[g.player - 1]
			bt = time.time()
			c = p.get_choice()
			g.move(c, g.player)
			if is_print:
				print("Spend time: %.2fs" % (time.time() - bt))
				g.print_board()
				print()
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

