import numpy as np
from utils import abs_pos_distance
class Agent:
    """
    strategy: None then its an honest voter otherwise the type of voting strategy to follow
    """
    def __init__(self,name):

        self.name = name
        self.strategy = False
        self.preference = []
        self.happiness = None

    
    def set_preference(self, preference=None, candidates=None):
        """
        Sets preferences of the candidates
        """
        if preference:
            self.preference = preference
        else:
            # initial random selection of preferences
            self.preference = np.random.permutation(candidates)
    
    def cal_happiness(self, env_result: list, vote: list):
        """
        Calculates agents individual happiness
        Parameters:
        - env_result (list): The voting result from environment
        - vote (list): The agents voting order for the candidates
        Returns:
        hapiness (float)
        """
        # calculate the distance
        raw_distances = abs_pos_distance(env_result, vote)
        print(f"[DEBUG]- raw_distances: {raw_distances}")
        x = 1/(1+np.array(raw_distances))
        print(f"[DEBUG]- x: {x}")
        alpha = np.ones_like(x)
        print(f"[DEBUG]- alpha: {alpha}")
        # happiness
        self.happiness = np.round(np.dot(alpha,x)/ np.sum(alpha),3)
        

    
    def set_vote(self, env_vot_scheme, env_preferences):
        """
        Sets the final vote based on the agents strategy
        env_vot_scheme: the voting scheme of the environment Ex: Borda
        env_preferences: Preferences of all the agents 

        """
        # if the agent is an honest agent then the vote and the preferences are same
        if not self.strategy:
            self.final_vote = self.preference
        else:
            # TODO: Based on the startegy manipulate vote
            pass


    

if __name__ == "__main__":
    agent = Agent('a1')
    agent.set_preference(preference=None, candidates=['c1','c2','c3','c4','c5','c6'])
    # print(agent.preference)
    # candidates=['c1','c2','c3','c4','c5','c6']
    # print(np.random.permutation(candidates))

    # test calculate happiness
    env_result = ['c1','c2','c3','c4','c5','c6']
    agent.cal_happiness(env_result, vote=agent.preference)
    print(f"prefernece: {agent.preference}, happiness: {agent.happiness}")