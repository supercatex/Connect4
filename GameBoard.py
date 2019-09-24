#!usr/bin/env python


class GameBoard(object):

	def __init__(self):
		self.num_of_players = 2
		self.rows = 6
		self.cols = 7
		self.chess_style = [" ", "○", "●"]
		self.last_chess_style = [" ", "①", "❷"]
		self.board = list()
		for i in range(self.rows):
			row_list = list()			
			for j in range(self.cols):
				row_list.append(0)
			self.board.append(row_list)
		self.player = 1
		self.records = list()

	def print_board(self):
		for i in range(self.rows):
			print("{} |".format(i + 1), end="")
			for j in range(self.cols):
				c = self.chess_style[self.board[i][j]]
				if len(self.records) > 0 and self.records[-1] == (i, j):
					c = self.last_chess_style[self.board[i][j]]
				print("{} ".format(c), end="")
			print("")
		print("  " + "==" * self.cols + "=")
		print("  ", end="")
		for i in range(self.cols):
			print(" {}".format(i + 1), end="")
		print("")

	def get_choices(self):
		choice_list = list()
		for i in range(self.cols):
			if self.board[0][i] == 0:
				choice_list.append(i)
		return choice_list

	def get_user_input(self):
		choices = self.get_choices()
		if len(choices) == 0:
			print("END GAME")
		else:
			c = input("Your turn:")
			if c.isdigit() and int(c) - 1 in choices:
				return int(c) - 1
			else:
				print("Wrong move!")
				return self.get_user_input()

	def move(self, choice, player):
		for i in range(self.rows-1, -1, -1):
			if self.board[i][choice] == 0:
				self.board[i][choice] = player
				self.records.append((i, choice))
				break

	def moveback(self):
		if len(self.records) == 0:
			return
		y, x = self.records.pop()
		self.board[y][x] = 0

	def next_player(self):
		self.player = self.player % self.num_of_players + 1

	def is_winner(self, last_choice, player):
		x = last_choice
		y = 0
		for i in range(self.rows):
			if self.board[i][x] == player:
				y = i
				break

		ax, ay = x, y
		bx, by = x, y
		while ax - 1 >= 0 and ay - 1 >= 0 and self.board[ay - 1][ax - 1] == player:
			ax -= 1
			ay -= 1
		while bx + 1 < self.cols and by + 1 < self.rows and self.board[by + 1][bx + 1] == player:
			bx += 1
			by += 1
		if bx - ax + 1 > 3:
			return True

		ax, ay = x, y
		bx, by = x, y
		while ax - 1 >= 0 and ay + 1 < self.rows and self.board[ay + 1][ax - 1] == player:
			ax -= 1
			ay += 1
		while bx + 1 < self.cols and by - 1 >= 0 and self.board[by - 1][bx + 1] == player:
			bx += 1
			by -= 1
		if bx - ax + 1 > 3:
			return True

		a = y
		b = y
		while b + 1 < self.rows and self.board[b + 1][x] == player:
			b += 1
		if b - a + 1 > 3:
			return True

		a = x
		b = x
		while a - 1 >= 0 and self.board[y][a - 1] == player:
			a -= 1
		while b + 1 < self.cols and self.board[y][b + 1] == player:
			b += 1
		if b - a + 1 > 3:
			return True

		return False

