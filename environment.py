from gym import Env
# from stable_baselines3.common.env_checker import check_env


class TradeEnv(Env):
    def __init__(self):
        self.action_space = None
        self.observation_space = None

    def step(self, action):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def render(self, mode=None):
        super.render()
        
    def close(self):
        raise NotImplementedError

    
        
        