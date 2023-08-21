from custom_environment import CustomEnvironment

from pettingzoo.test import parallel_api_test

import random

if __name__ == "__main__":
    print("test")
    env = CustomEnvironment()
    env.reset()
    for i in range(1000000):
        prisoner_action = random.randint(0,4)
        guard_action = random.randint(0,4)

        observations, rewards, terminations, truncations, infos = env.step({"prisoner": prisoner_action, "guard": guard_action})

        print(observations)

        env.render()
