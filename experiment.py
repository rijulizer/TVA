import numpy as np
from agent import Agent
from enviroment import Environment
from variables import env_candidates, env_vote_scheme
from utils import voting_scheme

class Experiment:

    def __init__(self, id, name):
        
        self.id = id
        self.name = name

    def set_exp_variables(
            self, 
            env_candidates : list[str] = ['c1','c2','c3','c4'], 
            env_vote_scheme: str = 'borda', 
            agent_vote_strategy : str = 'default',
            ):
        """
        Sets the experimental variables
        - env_candidates (list[str]): The list of candidates to vote for 
        - env_vote_scheme (str): The voting scheme used to calulate the result
        - agent_vote_strategy (str): The strategy used by strategic voter to manipulate voting
        Returns:
        list of agents (list)
        """
        
        self.agent_vote_strategy = env_candidates
        self.env_vote_scheme = env_vote_scheme 
        self.seagent_vote_strategy = agent_vote_strategy

    def create_agents(self, num_agents, num_strat_agents):
        """
        Creates agents
        - num_agents (int): The total number of agents to be created
        - num_strat_agents (int): number of strategic agents to be created
        Returns:
        list of agents (list)
        """
        assert num_strat_agents <= num_agents, "Number of strategic agents should not exceed total number of agents"
        agents = []
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
            print(f"Agent: {agent.name}, strategic_agent: {agent.strategy} preference: {agent.preference}\n")
        
        return agents
    
    def run_exp(self, exp_name: str, variables: list[str]):
        """

        Args:
            exp_name (str): _description_
            variables (list[str]): _description_
        """
            

if __name__ == "__main__":
    
    exp = Experiment(id=0, name='first_experiment')
    exp.create_agents(5, 1)
