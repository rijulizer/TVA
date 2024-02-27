import numpy as np
from agent import Agent
from variables import env_candidates



class Environment:
    def __init__(self,):
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = None
    
    def set_agent_preferences(self, agents: list):
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
    
    def cal_result(self,):
        """
        Calculates result of preferences and/or votes
        """
        self.result = {}
        # TODO: Implement the voting schemes here and 
        # based on the voting scheme, the calculation changes 
        # This logic is a place holder that depends on the voting scheme
        top_candidates = []
        for k,v in self.agent_prefs.items():
            top_candidates.append(v[0])
            # for c in v[0]:
            #     if c in self.result.keys():
            #         self.result[c] +=1
            #     else:
            #         self.result[c] =1
        return top_candidates#self.result
    
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
        agent.set_preference(env_candidates)
        agents.append(agent)

    env = Environment()
    env.set_agent_preferences(agents)

    print(env.agent_prefs)
    print(env.cal_result())
