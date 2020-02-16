
import argparse
from dsys.envs import LotkaVolterraEnv
from dsys.envs import OdeEnv
from matplotlib import pyplot as plt
import numpy as np
import os
from dsys.agents import generic
import tensorflow as tf
import tensorflow_probability as tfp


def lotka_volterra(t, X, alpha=1., beta=0.1, gamma=1.5, delta=0.75):
	""" Return the growth rate of fox and rabbit populations. """
	
	if len(X.shape) == 1:
		return np.array([
			alpha*X[0] - beta*X[0]*X[1], 
			-gamma*X[1] + delta*beta*X[0]*X[1]
		])
		
	else:
		
		Y = np.zeros(X.shape)
		Y[:,0] = alpha*X[:,0] - beta*X[:,0]*X[:,1]
		Y[:,1] = -gamma*X[:,1] + delta*beta*X[:,0]*X[:,1]
		
		return Y


if __name__ == "__main__":
	
	# Defaults...
	defaultNepochs = 10000
	
	# Parse the command line...
	parser = argparse.ArgumentParser(description='Openai gym lokta-volterra example.')
	parser.add_argument('--epochs', metavar='epochs', type=int, default=defaultNepochs,
		help='Number of epochs to run. Default {}'.format(defaultNepochs))
	parser.add_argument('--outdir', type=str, default='.', help="""Directory
		to save the output to that need not exist.  Default is the current
		directory""")
	parser.add_argument('--viz', action="store_true", help="""Visualize the
		the states of the environment""")
	
	args = parser.parse_args()
	
	# Create the output directory if necessary...
	if not os.path.isdir(args.outdir):
		os.makedirs(args.outdir)
	
	# Create the environment...
	ode_fns      = np.array([lotka_volterra])
	y_inits      = np.array([[1, 1]])
	t_inits      = np.array([0])
	t_steps      = np.array([15])
	num_ts       = np.array([100])
	error_models = np.array([tfp.distributions.LogNormal(loc=-1, scale=1)])
	
	env = OdeEnv(
		ode_fns,
		y_inits,
		t_inits,
		t_steps,
		num_ts,
		error_models=error_models
	)

	# Initial parameters for the Lotka-Volterra equations...
	init_params = (2./3., 4./3., 1., 1.) # alpha, beta, gamma, delta
	epsilon = 0.4
	
	# Create the agent...
	agent = generic.ParameterAdjustingAgent(
		init_params, epsilon, force_positive_params=True
	)
	
	# Book keeping for saving figures...
	pos_prev_reward = 1E100
	pos_med_reward_thresh = 100
	pos_low_reward_thresh = 5
	
	for epoch in range(args.epochs):
		
		milestone_epoch = (epoch % (.1 * args.epochs) == 0)
		if milestone_epoch:
			print("epoch {}".format(epoch))
			
		action, lv_params = agent.get_action()
		reward, env_state = env.step([lv_params])
		agent.update_Q(action, reward)
		
		if args.viz:
			
			# File name for recording the state of the figure.  Want to
			# record its state when the reward is in a particular state or at a
			# milestone epoch...
			pos_reward = abs(reward[0])
			figure_fname = None
			if milestone_epoch or \
					(pos_prev_reward < pos_low_reward_thresh and pos_reward >= pos_low_reward_thresh) or \
					(pos_prev_reward >= pos_low_reward_thresh and pos_reward < pos_low_reward_thresh) or \
					(pos_prev_reward < pos_med_reward_thresh and pos_reward >= pos_med_reward_thresh) or \
					(pos_prev_reward >= pos_med_reward_thresh and pos_reward < pos_med_reward_thresh):
				figure_fname = os.path.join(
					args.outdir,
					"env-state_epoch{}_reward{}.png".format(
						epoch, 
						str(reward[0]).replace(".", "p")
					)
				)
				

			env.render(figure_fname=figure_fname)
			
			# Only care about updating this when we're saving off figures. Dont
			# want it to go out of control when saving...
			pos_prev_reward = pos_reward
		

	print("Final parameters: {}".format(agent.get_parameters()))
	
	np.savetxt(
		os.path.join(args.outdir, "final-params.txt"),
		agent.get_parameters(),
		fmt="%.6f"
	)
