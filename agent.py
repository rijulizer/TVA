import numpy as np
class Agent:
    """
    strategy: None then its an honest voter otherwise the type of voting strategy to follow
    """
    def __init__(self,name):

        self.name = name
        self.strategy = None
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
    
    def cal_happiness(self,):
        """
        Calculates agents individual happiness
        """

        pass

    
    def set_vote(self, env_vot_scheme, env_preferences):
        """
        Sets the final vote based on the agents strategy
        env_vot_scheme: the voting scheme of the environment Ex: Borda
        env_preferences: Preferences of all the agents 

        """
        # if the agent is an honest agent then the vote and the preferences are same
        if not self.strategy:
            self.vote = self.preference
        else:
            # TODO: Based on the startegy manipulate vote
            pass


    

if __name__ == "__main__":
    agent = Agent('a1')
    agent.set_preference(preference=None, candidates=['c1','c2','c3','c4','c5','c6'])
    print(agent.get_preference())
    # candidates=['c1','c2','c3','c4','c5','c6']
    # print(np.random.permutation(candidates))