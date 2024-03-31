import numpy as np
from agent import Agent
from enviroment import Environment

from utils import map_vote, cal_result


class Experiment:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        print(f"exp_id: {self.id}, exp_name: {self.name}")

    def set_exp_variables(
            self, 
            env_candidates : list[str] = ['c1','c2','c3','c4'], 
            env_vote_scheme: str = 'borda', 
            agent_vote_strategy : str = 'compromising', #['compromising', 'bullet_voting', 'combination']
            happiness_type : str = 'A', #B, #C
            num_agents : int = 5, 
            num_strat_agents : int = 1
            ):
        """Sets the variables for each experiment [deprecated]

        Args:
            env_candidates (list[str], optional): list of candidates. Defaults to ['c1','c2','c3','c4'].
            env_vote_scheme (str, optional): the voying scheme. Defaults to 'borda'.
            agent_vote_strategy (str, optional): voting strategy. Defaults to 'compromising'.
            num_agents (int, optional): number of agents in the enviroment
            num_strat_agents (int, optional): number of strategic agents out of all the agents
        """
        
        self.env_candidates = env_candidates
        self.env_vote_scheme = env_vote_scheme 
        self.agent_vote_strategy = agent_vote_strategy
        self.happiness_type = happiness_type
        self.num_agents = num_agents
        self.num_strat_agents = num_strat_agents

    def run_single_exp(
            self, 
            env_candidates : list[str] = ['c1','c2','c3','c4'], 
            env_vote_scheme: str = 'borda', 
            agent_vote_strategy : str = 'compromising', #['compromising', 'bullet_voting', 'combination']
            happiness_type : str = 'A', #B, #C
            num_agents : int = 5, 
            num_strat_agents : int = 1
            ):
        """Runs a single experiment based on the parameters passed.

        Args:
            env_candidates (list[str], optional): list of candidates. Defaults to ['c1','c2','c3','c4'].
            env_vote_scheme (str, optional): the voying scheme. Defaults to 'borda'.
            agent_vote_strategy (str, optional): voting strategy. Defaults to 'compromising'.
            num_agents (int, optional): number of agents in the enviroment
            num_strat_agents (int, optional): number of strategic agents out of all the agents
        """
        # create environment
        env = Environment(
            env_candidates, 
            env_vote_scheme,
            agent_vote_strategy,
            happiness_type,
            num_agents,
            num_strat_agents,
        )
        # run environment
        env.run_tva()

    def run_multiple_exp(
            self,
            num_candidates: int = 5,
            voting_schemes: list[str] = ["plurality", "anti_plurality", "voting_for_two", "borda"],
            voting_strategies: list[str] = ['compromising', 'bullet_voting', 'combination'],
            hapiness_types: list[str] = ['A', 'B', 'C'],
            num_agents: int = 5,
            num_strat_agents: int = 1,
    ):
        env_candidates = [f"c{i}" for i in range(num_candidates)]
        print(f"Params:, \ncandidates: {env_candidates}, \nvoting schemes: {voting_schemes},\nvoting_strategies: {voting_strategies},\nhapiness_types: {hapiness_types}, \nnum_agents: {num_agents}, \nnum_strat_agents: {num_strat_agents}")
    
        for env_vote_scheme in voting_schemes:
            for agent_vote_strategy in voting_strategies:
                for happiness_type in hapiness_types:
                    # create environment
                    env = Environment(
                        env_candidates, 
                        env_vote_scheme,
                        agent_vote_strategy,
                        happiness_type,
                        num_agents,
                        num_strat_agents,
                    )
                    # run environment
                    env.run_tva()
                    # remove the object
                    del env

if __name__ == "__main__":
    
    # Create experiment
    exp = Experiment(id=0, name='first_experiment')
    # Run a single experiment
    # exp.run_single_exp(['c1','c2','c3','c4','c5'], 'borda', 'combination', 'B', 5, 1)
    
    # run sets of experiments
    exp.run_multiple_exp(
            num_candidates=5,
            voting_schemes=["plurality", "anti_plurality", "voting_for_two", "borda"],
            voting_strategies=['compromising', 'bullet_voting', 'combination'],
            hapiness_types=['A', 'B', 'C'],
            num_agents=5,
            num_strat_agents=1,
    )
        
