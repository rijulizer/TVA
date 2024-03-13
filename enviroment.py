import numpy as np
from agent import Agent
from variables import env_candidates, env_vote_scheme, agent_vote_strategy
from utils import voting_scheme
from pprint import pprint

class Environment:
    def __init__(self,):
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = None
    
    def collect_preferences(self, agents: list):
        """
        gets the preferences of all the agents
        """
        for a in agents:
            self.agent_prefs[a.name] = a.preference
    
    def set_agent_votes(self, agents: list):
        """
        gets the votes of all the agents
        """
        # TODO: this function should have the agent votes instead of preferences
        for a in agents:
            self.agent_prefs[a.name] = a.preference
    
    def cal_result(self):
        """
        Calculates result of preferences and/or votes
        """
        voting_output = voting_scheme(env_vote_scheme, self.agent_prefs)

        return voting_output
    
    def cal_total_happiness(self, agents: list):
        """
        Calculates the total hapiness of the system
        """
        for a in agents:
            self.total_happiness += a.happiness
        return self.total_happiness

if __name__ == "__main__":
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
        print(f"Agent: {agent.name}, strategic_agent: {agent.strategy}, preference: {agent.preference}\n")
    
    # define env
    env = Environment()
    env.collect_preferences(agents)
    # calculate initial result
    pprint(f"Agent preferences: {env.agent_prefs}")
    env_init_result, _ = env.cal_result()
    pprint(f"Voting result Dict: {env_init_result}")

    # # Set the vote for the strategic agent
    agents[0].set_vote(env_vote_scheme, agent_vote_strategy, env_init_result, env.agent_prefs)
