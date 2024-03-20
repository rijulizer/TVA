import numpy as np
from utils import voting_scheme, cal_happiness, map_vote, cal_result
from pprint import pprint
from itertools import combinations, permutations
class Agent:
    """
    strategy: None then its an honest voter otherwise the type of voting strategy to follow
    """
    def __init__(self,name):

        self.name = name
        self.strategy = False
        self.real_preference = []
        # self.happiness = 0
        self.best_pref = []
        self.final_vote = []

    
    def set_preference(self, preference=None, candidates=None):
        """
        Sets preferences of the candidates
        """
        if preference:
            self.real_preference = preference
        else:
            # initial random selection of preferences
            self.real_preference = np.random.permutation(candidates).tolist()

    def set_vote(self, 
                 env_vote_scheme,
                 env_candidates, 
                 agent_vote_strategy, 
                 env_result, 
                 env_agent_prefs,
                 env_agent_votes,
            ):
        """
        Sets the final vote based on the agents strategy to maximize self happiness. Only strategic agent can use this function
        env_vote_scheme: the voting scheme of the environment Ex: Borda
        env_result: Result of the voting round
        env_agent_prefs: preferences of all the agents (from the env)

        """

        # Assign some variables to make condition checking easier
        compromising = (agent_vote_strategy == "compromising" or agent_vote_strategy == "combination")
        bullet_voting = (agent_vote_strategy == "bullet_voting" or agent_vote_strategy == "combination")

        # TODO:Only the strategic agent can set_vote
        # if the agent is an honest agent then the vote and the preferences are same
        if not self.strategy:
            # self.final_vote = self.real_preference
            raise NotImplementedError("Non strategic agent sould not call this function")
        else:
            if compromising:
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
                hap_init = cal_happiness(env_result_list, self.real_preference)
                print(f"[Debug]-[set_vote]- hap_init: {hap_init}")
                max_hap = hap_init
                best_pref = self.real_preference
                strategic_voted = False
                best_vote = map_vote(env_vote_scheme, env_candidates, best_pref, bullet_voting)
                # get all possible voting options
                all_combos = list(set(permutations(best_pref, len(best_pref))))
                for comb in all_combos:
                    # for only the strategic agent change the perefence
                    env_agent_prefs[self.name] = list(comb)
                    # generate vote from preference order
                    env_agent_votes[self.name] = map_vote(env_vote_scheme, env_candidates, list(comb), bullet_voting)
                    # calculate result of the new votes
                    voting_output, voting_output_list = cal_result(env_candidates, env_agent_votes)
                    # calculate happiness, check the happiness wrt, the real_preference
                    happiness = cal_happiness(voting_output_list, self.real_preference)
                    # print(f"[Debug]-[set_vote]- pref: {list(comb)}, voting_output: {voting_output}, happiness: {happiness}")
                    if happiness > max_hap:
                        strategic_voted = True
                        max_hap = happiness
                        best_pref = list(comb)
                        best_vote = map_vote(env_vote_scheme, env_candidates, list(comb), bullet_voting)
                        print(f"[Debug]-[set_vote]- max_hap: {max_hap}, best_pref: {best_pref}, best_vote: {best_vote}\n")
                        
                self.final_vote = best_vote
                self.best_pref = best_pref
                        
            elif bullet_voting:
                strategic_voted = True
                bullet_vote = map_vote(env_vote_scheme, env_candidates, self.real_preference, bullet_voting)
                # generate vote from preference order
                env_agent_votes[self.name] = bullet_vote
                # calculate result of the new votes
                voting_output, voting_output_list = cal_result(env_candidates, env_agent_votes)
                # calculate happiness, check the happiness wrt, the real_preference
                happiness = cal_happiness(voting_output_list, self.real_preference)
                print(f"[Debug]-[set_vote]- pref: {self.real_preference}, voting_output: {voting_output}, happiness: {happiness}, bullet vote: {bullet_vote}\n")

                self.best_pref = self.real_preference
                self.final_vote = bullet_vote

            else:
                raise NotImplementedError("Strategist doesnt use a valid strategy")

            print(f"[Debug]-[set_vote]- strategic_voted: {strategic_voted}\n")
                
if __name__ == "__main__":
    # Test create agent 
    agent = Agent('a1')
    agent.set_preference(preference=None, candidates=['c1','c2','c3','c4','c5','c6'])
    print(agent.real_preference)
    # # candidates=['c1','c2','c3','c4','c5','c6']
    # # print(np.random.permutation(candidates))

    # test calculate happiness
    env_result = ['c1','c2','c3','c4','c5','c6']
    # preference = ['c1','c2','c3','c4','c5','c6']
    # happiness = agent.cal_happiness(env_result, preference)
    # print(f"prefernece: {preference}, happiness: {happiness}")
    happiness = cal_happiness(env_result, agent.real_preference)
    print(f"real_prefernece: {agent.real_preference},\nresult: {env_result}, \nhappiness: {happiness}")


    # Function which returns subset or r length from n
    # arr =['c1','c2','c3']
    # for comb in list(set(permutations(arr, len(arr)))):
    # print(list(comb))