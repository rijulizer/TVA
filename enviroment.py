import numpy as np
from agent import Agent
from variables import env_candidates, env_vote_scheme
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
    for i in range(5):
        agent = Agent(f'a{i}')
        agent.set_preference(candidates = env_candidates)
        print(f"Agent: {agent.name}, preference: {agent.preference}\n")
        agents.append(agent)
    # set rqandom preferene agents
    env = Environment()
    env.collect_preferences(agents)

    # pprint(f"Agent preferneces: {env.agent_prefs}")
    pprint(f"Voting result: {env.cal_result()}")
