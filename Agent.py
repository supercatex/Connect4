#!usr/bin/env python
import random
import copy
from GameBoard import GameBoard
import numpy as np


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
	def __init__(self, name, player, game, max_depth=3):
		super(NStepAgent, self).__init__(name, player, game)
		self.max_depth = max_depth

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
		v, c = self.minmax(self.max_depth, copy.deepcopy(self.game))
		if c is not None:
			return c
		return random.choice(self.game.get_choices())


class Action(object):

	def __init__(self, choice, previous_action=None):
		self.choice = choice
		self.previous_action = previous_action
		self.next_actions: Action = []
		self.simulations = 0
		self.winners = 0

	def get_next_action(self, choice):
		for na in self.next_actions:
			if na.choice == choice:
				return na
		return None

	def get_UCT(self):
		dict = {}
		t = self.simulations
		for a in self.next_actions:
			w = a.winners
			n = a.simulations
			if n > 0:
				uct = w / n + np.sqrt(2 * np.log10(t) / n)
			else:
				uct = 0
			dict[a.choice] = uct
		return dict

	def make_action(self, choice):
		if self.get_next_action(choice) is None:
			self.next_actions.append(Action(choice, self))

	def __str__(self):
		s = ""
		for na in self.next_actions:
			s += str(na.choice) + " "
		return s


class UCTAgent(RandomAgent):

	def __init__(self, name, player, game):
		super(UCTAgent, self).__init__(name, player, game)
		self.current_action = Action(0)
		self.agent = NStepAgent(name, player, game)

	def random_walk(self, depth=0):
		player = (self.player + depth + 1) % 2 + 1
		choices = self.game.get_choices()
		if len(choices) == 0:
			return 0

		c = random.choice(choices)
		self.current_action.make_action(c)
		self.current_action.simulations += 1
		self.current_action = self.current_action.get_next_action(c)

		self.game.move(c, player)
		self.game.next_player()
		# self.game.print_board()

		result = 0
		if self.game.is_winner(c, player):
			self.game.moveback()
			self.game.next_player()
			if player == self.player:
				result = 1
		else:
			result = self.random_walk(depth + 1)
			self.game.moveback()
			self.game.next_player()

		self.current_action = self.current_action.previous_action
		self.current_action.winners += result
		return result

	def get_choice(self):
		# v, c = self.agent.minmax(3, copy.deepcopy(self.game))
		# if c is not None:
		# 	self.current_action.make_action(c)
		# 	self.current_action = self.current_action.get_next_action(c)
		# 	return c

		for i in range(1000):
			self.random_walk()
		uct = self.current_action.get_UCT()
		choice = max(uct, key=uct.get)
		self.current_action = self.current_action.get_next_action(choice)
		return choice
