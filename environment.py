import functools
import random
from copy import copy
import math
import mixbox
import random

import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete

from pettingzoo.utils.env import ParallelEnv


class CustomEnvironment(ParallelEnv):
    metadata = {
        "name": "colourwheel_v0",
    }

    def __init__(self, length):
        # init agents
        self.possible_agents = ["worker_r", "worker_g", "worker_b"]
        
        for i in range(length):
            
            agent_name = self.possible_agents[random.randint(2)] + "_" + i
            self.possible_agents.append(agent_name)

        self.line_length = length

    def reset(self, num_products=2, seed=None, options=None):
        self.agents = copy(self.possible_agents)
        self.timestep = 0
        self.num_products = num_products
        self.products = []

        # init products on line
        for i in range(self.num_products):
            self.products.append(Product())

        # define global and local observations
        observations = self._generate_local_observations()
        return observations, {}

    def step(self, actions):
        
        # Loop through products and colorize
        for product in self.products:
            product.mix(actions[product.position], actions[product.position-1])

            if product.position >= self.line_length:
                #calculate reward
                rewards = self._compute_reward()
            
            else:
                product.position += 1

        # Get observations
        observations = self._generate_local_observations()

        return observations, rewards

    def render(self):
        
        # TODO figure out render method
        pass

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # TODO figure out observation dims
        
        pass

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # each type of agent can choose to contribute 10 levels of the given colour to the addition 
        return Discrete(10)

    def _generate_local_observations(self):

        partial_observations = {
            product.position:  (
                [
                    product.current_color, 
                    product.desired_color, 
                    product.num_rounds
                ]
            )
            for product in self.products
        }
        observations = {
             agent: (
                None if index not in partial_observations.keys else partial_observations{index}
            )
            for index, agent in enumerate(self.agents)
        }
        return observations, {}

    def _compute_reward():
    	# TODO figure out reward mechanism
        pass


class Product():
    def __init__(self, starting_position, current_rgb, desired_rgb):

        self.current_rgb = current_rgb
        self.desired_rgb = desired_rgb

        self.position = starting_position
        self.num_rounds = 0

    def mix(self, color1, color2, ratio1=0.5, ratio2=0.5):
        # cmyk colour mixing

        rgb_mix = mixbox.lerp(color1, color2, ratio1)
        self.current_rgb = mixbox.lerp(self.current_rgb, rgb_mix, ratio2)
