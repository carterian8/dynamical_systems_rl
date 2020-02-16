
import gym
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import sys
# import tensorflow as tf
# import tensorflow_probability as tfp


class OdeEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(
			self,
			ode_fns,
			y_inits,
			t_inits,
			t_steps,
			num_ts,
			error_models
	):
		"""
		TODO: Write description
		"""

		if (ode_fns.shape[0] != y_inits.shape[0] != \
				t_inits.shape[0] != t_steps.shape[0] != num_ts.shape[0]):
			
			raise ValueError("""The number of couplings (ode_fns), their initial 
				values (y_inits), their start times (t_inits), step size 
				(t_steps), and their number of solve points (num_ts) must have
				an equal number of rows""")

		self.ode_fns      = ode_fns
		self.y_inits      = y_inits
		self.t_init_origs = t_inits
		self.t_inits      = t_inits
		self.t_steps      = t_steps
		self.num_ts       = num_ts
		self.error_models = error_models
		self.figs         = [None] * ode_fns.shape[0]
		self.prev_ys      = [None] * ode_fns.shape[0]
		self.figlines     = [None] * ode_fns.shape[0]
		
		# Enable matplotlib.pyplot interactive mode
		plt.ion()
		
	
	def step(self, action):
		
		# Generate solution times...
		t_finals = self.t_inits + self.t_steps
		solution_times = np.linspace(
			self.t_inits, t_finals, self.num_ts, axis=1
		)
		
		# Evaluate the ode(s)...
		ode_fns_results = []
		rewards = np.zeros(len(self.ode_fns))
		
		for i in range(len(self.ode_fns)):
			self.prev_ys[i], info_dict = odeint(
				self.ode_fns[i],
				self.y_inits[i],
				solution_times[i],
				args=action[i],
				full_output=True,
				tfirst=True
			)
			
			ode_fns_results.append((self.prev_ys[i], info_dict))
			
			# Find the value of the derivative at each point..
			derivatives = self.ode_fns[i](
				solution_times[i], self.prev_ys[i], *action[i]
			)
			
			# The score given is relative to the magnitude of the derivative
			# at each of the solutions
			rewards[i] = -np.sum(np.abs(derivatives))

			# Want solutions to be close to the initial conditions so reward
			# solutions that are close to them...
			rewards[i] = -np.log(
				np.maximum(
					np.ones(rewards.shape),
					np.abs(rewards[i] - 1000 * np.sum(np.abs(self.prev_ys[i] - self.y_inits[i])))
				)
			)
			
			
		# NaNs can happen when parameters are given which violate properties of
		# the ode_fns.  Check if this has happened and adjust the reward
		# appropriately...
		nan_check = np.isnan(rewards)
		if nan_check[nan_check == True].shape[0] > 0:
			print("DEBUG: Hit NaN")
			rewards[nan_check == True] = -10.
			print(rewards)
			
		# Increment the next starting time...
		self.t_inits = self.t_inits + self.t_steps
		
		
		return rewards, ode_fns_results
		
	def reset(self):
	
		# Set the initial time back to the original initial time
		self.t_inits = self.t_init_origs
		
	def render(self, mode='human', figure_fname=None):
		
		# Plot the previous solutions to each equation describing the coupling..
		for ode_fn_idx in range(0, self.ode_fns.shape[0]):
		
			if self.figs[ode_fn_idx] is None:
				# Create a figure for this coupling...
				self.figs[ode_fn_idx] = plt.figure()
				
				if self.prev_ys[ode_fn_idx] is not None:
					# The ODE describing this coupling has been evaluated so 
					# update the plot data...
					ax = self.figs[ode_fn_idx].add_subplot(111)
					self.figlines[ode_fn_idx] = [None] * self.prev_ys[ode_fn_idx].shape[1]
					for i in range(self.prev_ys[ode_fn_idx].shape[1]):
						figline, = ax.plot(self.prev_ys[ode_fn_idx][:,i])
						self.figlines[ode_fn_idx][i] = figline
			
			if self.figlines[ode_fn_idx] is not None and \
					self.prev_ys[ode_fn_idx] is not None:
				# Something has already been drawn for this coupling and there
				# is new data to draw; update the plot...
				
				for i in range(self.prev_ys[ode_fn_idx].shape[1]):
					self.figlines[ode_fn_idx][i].set_ydata(self.prev_ys[ode_fn_idx][:,i])
				self.figs[ode_fn_idx].canvas.draw()
				self.figs[ode_fn_idx].canvas.flush_events()
				plt.show()
				
				if figure_fname is not None:
					plt.savefig(figure_fname)

	def close(self):
		pass
		
