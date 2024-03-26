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
        """Sets the variables for each experiment

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

    
    def run_exp(self):
        # Step-0: Create environment
        # Step-1: Get all agents preferences and votes
        # Step-2: Calculate inital result
        # Step-3: Stategic agent sets votes
        
        # create environment
        env = Environment(
            self.env_candidates, 
            self.env_vote_scheme,
            self.agent_vote_strategy,
            self.happiness_type,
            self.num_agents,
            self.num_strat_agents,
        )
        env.collect_prefs_and_votes()
        # calculate initial result
        env_init_result, env_init_result_list = cal_result(env.env_candidates, env.agent_votes)
        print(f"Initial voting result Dict: {env_init_result}")

        # initial happiness
        env.cal_total_happiness(env_init_result_list)
        print(f"Initial Total Happiness: {env.total_happiness}")
        init_total_happiness = env.total_happiness
        print(f"[Debug]-[Exp]- init_total_happiness: {init_total_happiness}")

        # Set the vote for the strategic agent
        # # Set the vote for the strategic agent
        env.agents[0].set_vote(
                env.env_vote_scheme,
                env.env_candidates, 
                env.agent_vote_strategy, 
                env.happiness_type,
                env_init_result, 
                env.agent_prefs,
                env.agent_votes,
            )
        print(f"[Debug]-[Env]- Best vote: {env.agents[0].final_vote} \n Best pref: {env.agents[0].best_pref}")
        
        # collect final votes and preferences
        env.collect_prefs_and_votes()
        # calculate final result
        env_final_result, env_final_result_list = cal_result(env.env_candidates, env.agent_votes)
        print(f"Final voting result Dict: {env_final_result}")

        env.cal_total_happiness(env_final_result_list)
        print(f"Final Total Happiness: {env.total_happiness}")
        final_total_happiness = env.total_happiness
        print(f"[Debug]-[Exp]- final_total_happiness: {final_total_happiness}")


        # TODO RISK

        return init_total_happiness, final_total_happiness

if __name__ == "__main__":
    
    # Create experiment
    print("#"*50)
    exp = Experiment(id=0, name='first_experiment')

    # Set experiment variables
    exp.set_exp_variables(['c1','c2','c3','c4','c5'], 'borda', 'combination', 'B', 5, 1)
    
    exp.run_exp()
