import numpy as np
from utils import abs_pos_distance, voting_scheme
from pprint import pprint
from itertools import combinations, permutations
class Agent:
    """
    strategy: None then its an honest voter otherwise the type of voting strategy to follow
    """
    def __init__(self,name):

        self.name = name
        self.strategy = False
        self.preference = []
        # self.happiness = None

    
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
        # print(f"[DEBUG]-[cal_happiness] raw_distances: {raw_distances}")
        x = 1/(1+np.array(raw_distances))
        # print(f"[DEBUG]-[cal_happiness] x: {x}")
        alpha = np.ones_like(x)
        # print(f"[DEBUG]-[cal_happiness]- alpha: {alpha}")
        # happiness
        happiness = np.round(np.dot(alpha,x)/ np.sum(alpha),3)
        # self.happiness = happiness
        return happiness

        

    
    def set_vote(self, 
                 env_vote_scheme, 
                 agent_vote_strategy, 
                 env_result, 
                 env_agent_prefs,
            ):
        """
        Sets the final vote based on the agents strategy to maximize self happiness
        env_vote_scheme: the voting scheme of the environment Ex: Borda
        env_result: Result of the voting round
        env_agent_prefs: preferences of all the agents

        """
        # TODO:Only the strategic agent can set_vote
        # if the agent is an honest agent then the vote and the preferences are same
        if not self.strategy:
            self.final_vote = self.preference
        else:
            # TODO: Based on the startegy manipulate vote
            # if agent_vote_strategy== "basic": #TODO: this term is not right
            # step-1: Calculate initial happiness based in self preference
            # step-2: remove inital preference from the result (not needed here)
            # step-3: Iterate over all the possibilities (This is one simple strategy)
                #step-3.1: calculate result of the voting
                #step3.2: Calculate happiness
                #step3.3: check max of happiness, store vote that leads to max happiness
            # step-4: send the final vote

            # getting a list of candidates from dictionary
            env_result_list = list(sorted(env_result, key=env_result.get, reverse=True))
            # print(f"[Debug]-[set_vote]- env_result_list: {env_result_list}")
            # calculate initial happiness
            hap_init = self.cal_happiness(env_result_list, self.preference)
            print(f"[Debug]-[set_vote]- hap_init: {hap_init}")
            max_hap = hap_init
            best_vote = self.preference
            # get all possible voting options
            all_combos = list(set(permutations(best_vote, len(best_vote))))
            for comb in all_combos:
                # for only the strategic agent change the perefence
                env_agent_prefs['self.name'] = list(comb)
                # calculate result
                voting_output,_ = voting_scheme(env_vote_scheme, env_agent_prefs)
                # calculate happiness
                voting_output_list = list(sorted(voting_output, key=voting_output.get, reverse=True))
                happiness = self.cal_happiness(env_result=voting_output_list, vote=list(comb))
                print(f"[Debug]-[set_vote]- vote: {list(comb)}, voting_output: {voting_output}, happiness: {happiness}")
                if happiness > max_hap:
                    max_hap = happiness
                    best_vote = list(comb)
                    print(f"[Debug]-[set_vote]- max_hap: {max_hap}, best_vote: {best_vote}")
                
                
            self.final_vote = best_vote
                

        

if __name__ == "__main__":
    pass
    agent = Agent('a1')
    agent.set_preference(preference=None, candidates=['c1','c2','c3','c4','c5','c6'])
    # # print(agent.preference)
    # # candidates=['c1','c2','c3','c4','c5','c6']
    # # print(np.random.permutation(candidates))

    # test calculate happiness
    env_result = ['c1','c2','c3','c4','c5','c6']
    preference = ['c1','c2','c3','c4','c5','c6']
    agent.cal_happiness(env_result, preference)
    print(f"prefernece: {preference}, happiness: {agent.happiness}")

    # agent.cal_happiness(env_result, vote=agent.preference)
    # print(f"prefernece: {agent.preference}, happiness: {agent.happiness}")


    # Function which returns subset or r length from n
    # arr =['c1','c2','c3']
    # for comb in list(set(permutations(arr, len(arr)))):
    # print(list(comb))