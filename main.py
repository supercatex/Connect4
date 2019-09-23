#!usr/bin/env python

from GameBoard import *
from Agent import *


if __name__ == "__main__":
	p1 = 0
	p2 = 0
	for i in range(100000):
		g = GameBoard()
		#g.print_board()

		players = [TwoStepAgent("COM1", 1, g), TwoStepAgent("COM2", 2, g)]
		
		while len(g.get_choices()) > 0:
			p = players[g.player - 1]
			c = p.get_choice()
			g.move(c, g.player)
			#g.print_board()
			if g.is_winner(c, g.player):
				#print(p.name + " is WINNER!")
				if p.player == 1:
					p1 += 1
				if p.player == 2:	
					p2 += 1
				break
			g.next_player()
		print("%.4f, %.4f, %.4f, %d" % (p1 / (i + 1), p2 / (i + 1), (i + 1 - p1 - p2) / (i + 1), i + 1))

