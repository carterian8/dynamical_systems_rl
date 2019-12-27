
import math
import numpy as np

# Modified from original source:
#	https://github.com/ankonzoid/LearningX/blob/master/classical_RL/MAB/MAB.py
class ParameterAdjustingAgent:
	"""
	DESCRIPTION:
		This is an epsilon greedy agent which, for each parameter describing
		a coupling equation of one or more random variables, chooses to  
		either increment, decrement, or keep the parameter the same. 
	"""

	def __init__(
		self, 
		initial_parameters, 
		epsilon, 
		learning_rate=0.1,
		discount_factor=0,
		force_positive_params=False
	):
		self.epsilon = epsilon
		self.parameters = initial_parameters if type(initial_parameters) == list() else list(initial_parameters)
		self.learning_rate = learning_rate
		self.discount_factor = discount_factor
		self.num_actions_for_param = 3
		self.total_num_actions = self.num_actions_for_param * len(initial_parameters)
		self.k = np.zeros(self.total_num_actions, dtype=np.int)  # number of times action was chosen
		self.Q = np.zeros(self.total_num_actions, dtype=np.float)  # estimated value
		self.force_pos_params = force_positive_params

	def update_Q(self, action, reward):
		self.k[action] = self.k[action] + 1  # update action counter k -> k+1
		prediction = 0
		learned_value = reward + (self.discount_factor * prediction)
		self.Q[action] = self.Q[action] + self.learning_rate * (learned_value - self.Q[action])
		

	# Choose action using an epsilon-greedy agent
	def get_action(self, force_explore=False):
		rand = np.random.random()  # [0.0,1.0)
		action = -1
		if (rand < self.epsilon) or force_explore:
			# randomly decide an action for a parameter
			action = np.random.randint(self.total_num_actions)

		else:
			# Exploit the best current parameter
			try:
				action = np.random.choice(np.flatnonzero(self.Q == self.Q.max()))
			except:
				import sys
				print(self.Q)
				print(self.Q.max())
				print(self.Q == self.Q.max())
				print(np.flatnonzero(self.Q == self.Q.max()))
				sys.exit()
				
		# Find out which parameter this action corresponds to then add/subtract
		# or do nothing to it
		parameter = int(math.floor(action / float(self.num_actions_for_param)))

		rand_val = 0
		mod = action % self.num_actions_for_param
		if mod == 0:
			rand_val = -.1 #-np.random.random()
		elif mod == 2:
			rand_val = .1 #np.random.random()
		
		updated_param = self.parameters[parameter] + (rand_val )
		self.parameters[parameter] = max(0.0, updated_param) \
			if self.force_pos_params else updated_param
		
		return action, tuple(self.parameters)

	def get_parameters(self):
		return self.parameters
