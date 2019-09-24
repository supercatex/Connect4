#!usr/bin/env python
import random
import copy


class Agent(object):
	
	def __init__(self, name, player, game):
		self.name = name
		self.player = player
		self.game = game

	def get_choice(self):
		return self.game.get_user_input()


class RandomAgent(Agent):
	def get_choice(self):
		return random.choice(self.game.get_choices())


class OneStepAgent(RandomAgent):
	def best_choice(self, player):
		g = copy.deepcopy(self.game)
		choices = g.get_choices()
		for c in choices:
			g.move(c, player)
			if g.is_winner(c, player):
				g.moveback()
				return c
			g.moveback()
		return None

	def get_choice(self):
		c = self.best_choice(self.player)
		if c is not None:
			return c

		return super().get_choice()


class TwoStepAgent(OneStepAgent):
	def best_choice(self, player):
		c = super().best_choice(player)
		if c is not None:
			return c
		g = copy.deepcopy(self.game)
		choices = g.get_choices()
		for c in choices:
			g.move(c, player % 2 + 1)
			if g.is_winner(c, player % 2 + 1):
				g.moveback()
				return c
			g.moveback()
		return None


class NStepAgent(OneStepAgent):
	def minmax(self, depth, g, alpha=-9999, beta=9999, is_your_turn=True):
		if depth == 0:
			return 0, None

		if len(g.records) > 0:
			last_move = g.records[-1][1]
			if g.is_winner(last_move, g.player % 2 + 1):
				if not is_your_turn:
					return 100, None
				else:
					return -100, None

		choices = g.get_choices()
		random.shuffle(choices)
		best_choice = None
		best_val = -9999
		if not is_your_turn:
			best_val = -best_val

		for c in choices:
			g.move(c, g.player)
			g.next_player()
			val, choice = self.minmax(depth - 1, g, alpha, beta, not is_your_turn)
			g.moveback()
			g.next_player()

			if is_your_turn:
				if val > best_val:
					best_val = val
					best_choice = c
					alpha = val
					if beta <= alpha:
						break
			else:
				if val < best_val:
					best_val = val
					best_choice = c
					beta = val
					if beta <= alpha:
						break

		return best_val, best_choice
		
	def get_choice(self):
		v, c = self.minmax(10, copy.deepcopy(self.game))
		if c is not None:
			return c
		return random.choice(self.game.get_choices())
