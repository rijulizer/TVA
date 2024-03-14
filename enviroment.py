import numpy as np
from agent import Agent
from variables import env_candidates, env_vote_scheme, agent_vote_strategy
from utils import voting_scheme, map_vote
from pprint import pprint

class Environment:
    def __init__(self,):
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = None
    
    def collect_prefs_and_votes(self, agents: list):
        """
        gets the preferences of all the agents
        """
        for a in agents:
            # get preferences
            self.agent_prefs[a.name] = a.real_preference
            # get votes
            self.agent_votes[a.name] = map_vote(env_vote_scheme, a.real_preference)
    
    # def set_agent_votes(self, agents: list):
    #     """
    #     gets the votes of all the agents
    #     """
    #     # TODO: this function should have the agent votes instead of preferences
    #     for a in agents:
    #         self.agent_prefs[a.name] = a.real_preference
    
    def cal_result(self, votes):
        """
        Calculates result of preferences and/or votes
        """
        inital_result = {}
        # iterate all the agent votes
        for vote in votes.values():
            # iterates all the candidates
            for c_index, c_val in enumerate(env_candidates):
                # check if the candidate is a key in the inital_result
                if c_val in inital_result.keys():
                    # add the vote of the candidate
                    inital_result[c_val] += vote[c_index]
                else:
                    inital_result[c_val] = vote[c_index]
        
        # sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
        # Sort based on the reverse of values and alphabatical order of keys
        sorted_dict = dict(sorted(inital_result.items(), key=lambda item:(-item[1],item[0])))
        
        sorted_list = list(sorted(inital_result, key=inital_result.get, reverse=True))



        return sorted_dict, sorted_list
    
    # def cal_total_happiness(self, agents: list):
    #     """
    #     Calculates the total hapiness of the system
    #     """
    #     for a in agents:
    #         self.total_happiness += a.happiness
    #     return self.total_happiness

if __name__ == "__main__":
    env_vote_scheme = 'plurality'
    agents = []
    num_agents = 5
    num_strat_agents = 1
    # create and define agents
    for i in range(num_agents):
            # instantiate agent objects
            agent = Agent(f'agent_{i}')
            # set agent preferences randomly
            agent.set_preference(candidates = env_candidates)
            agents.append(agent)
    for i in range(num_strat_agents):
        # make these agents strategic
        agents[i].strategy = True
    
    for agent in agents: # DEBUG
        pprint(f"Agent: {agent.name}, strategic_agent: {agent.strategy}, preference: {agent.real_preference}")
    print("#"*50)
    # test define env
    env = Environment()
    env.collect_prefs_and_votes(agents)
    # calculate initial result
    pprint(f"Agent preferences: {env.agent_prefs}")
    pprint(f"Agent votes: {env.agent_votes}")
    env_init_result, _ = env.cal_result(env.agent_votes)
    pprint(f"Voting result Dict: {env_init_result}")

    # # Set the vote for the strategic agent
    # agents[0].set_vote(env_vote_scheme, agent_vote_strategy, env_init_result, env.agent_prefs)
    # print(f"[Debug]-[Env]- Best vote: {agents[0].best_vote}")