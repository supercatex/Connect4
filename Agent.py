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
	def minmax(self, depth, g):
		if depth == 2:
			return None

		if depth % 2 == 0:
			c = self.best_choice(g.player)
			if c is not None:
				return c

			choices = g.get_choices()
			for c in choices:
				g.move(c, g.player)
				g.next_player()
				cc = self.minmax(depth + 1, g)
				if cc is not None:
					g.moveback()
					g.next_player()
					return cc
				g.moveback()
				g.next_player()
		else:
			c = self.best_choice(g.player)
			if c is not None:
				return None

			choices = g.get_choices()
			for c in choices:
				g.move(c, g.player)
				g.next_player()
				cc = self.minmax(depth + 1, g)
				if cc is not None:
					g.moveback()
					g.next_player()
					return cc
				g.moveback()
				g.next_player()

		return None
		
	def get_choice(self):
		c = self.minmax(0, copy.deepcopy(self.game))
		if c is not None:
			return c
		return random.choice(self.game.get_choices())


