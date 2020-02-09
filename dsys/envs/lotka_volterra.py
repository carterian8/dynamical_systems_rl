import gym
from gym import error, spaces, utils
from gym.utils import seeding
from matplotlib import pyplot as plt
import numpy as np
import numpy.random as npr
from scipy import integrate

class LotkaVolterraEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, nt=300):
		self.nt = nt
		
		self.reset()
	
	def step(self, action):
	
		def lotka_volterra(X, t=0, a = 1., b = 0.1, c = 1.5, d = 0.75):
			""" Return the growth rate of fox and rabbit populations. """
			return np.array([a*X[0] - b*X[0]*X[1], -c*X[1] + d*b*X[0]*X[1]])
		
		t0 = self.t
		t1 = self.t + self.twin
		t = np.linspace(self.t, t1, self.nt)   # time
		y0 = np.array([10, 5])          # initials conditions: 10 rabbits and 5 foxes
		outputs, info_dict = integrate.odeint(
			func=lotka_volterra,
			y0=y0,
			t=t,
			rtol=1e-6,
			atol=1e-6,
			full_output=True,
		)
		
		# Update the time interval
		self.t = t1
		
		return outputs, t
		
	def reset(self):
		self.t = 0
		self.twin = 15
		self.samps = 0
		
	def render(self, mode='human'):
		...

	def close(self):
		...
		
