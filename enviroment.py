import numpy as np
from agent import Agent
from utils import voting_scheme, map_vote, cal_result
from pprint import pprint

class Environment:
    def __init__(
        self,
        env_candidates : list[str] = ['c1','c2','c3','c4'], 
        env_vote_scheme: str = 'borda', 
        agent_vote_strategy : str = 'compromising', #['compromising', 'bullet_voting', 'combination']
        num_agents : int = 5, 
        num_strat_agents : int = 1,
        ):
        
        self.env_candidates = env_candidates
        self.env_vote_scheme = env_vote_scheme 
        self.agent_vote_strategy = agent_vote_strategy
        self.num_agents = num_agents
        self.num_strat_agents = num_strat_agents
        
        self.agents = []
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = None
        
        # create and define agents
        for i in range(num_agents):
                # instantiate agent objects
                agent = Agent(f'agent_{i}')
                # set agent preferences randomly
                agent.set_preference(candidates = self.env_candidates)
                self.agents.append(agent)
        for i in range(num_strat_agents):
            # make these agents strategic
            self.agents[i].strategy = True
        
        for agent in self.agents: # DEBUG
            pprint(f"[DEBUG]-[Env]- Agent: {agent.name}, strategic_agent: {agent.strategy}, preference: {agent.real_preference}")
        
    def collect_prefs_and_votes(self):
        """
        Collects the preferences and votes of all the agents in the env
        """
        for a in self.agents:
            # get preferences
            self.agent_prefs[a.name] = a.real_preference
            # get votes
            self.agent_votes[a.name] = map_vote(self.env_vote_scheme, self.env_candidates, a.real_preference)
        pprint(f"[DEBUG]-[Env], votes: {self.agent_votes}")
   
    def cal_total_happiness(self):
        """Calculates the total hapiness of the system
        """
        
        for a in self.agents:
            self.total_happiness += a.happiness
        return self.total_happiness

if __name__ == "__main__":
    # env_vote_scheme = 'borda'
    # agent_vote_strategy = 'combination'
    # num_agents : int = 5, 
    # num_strat_agents : int = 1,

    # test define env
    env = Environment(['c1','c2','c3','c4'], 'borda', 'combination', 5,1)
    env.collect_prefs_and_votes()

    print("#"*50)
    # calculate initial result
    # pprint(f"Agent preferences: {env.agent_prefs}")
    # pprint(f"Agent votes: {env.agent_votes}")
    env_init_result, _ = cal_result(env.env_candidates, env.agent_votes)
    pprint(f"Inital voting result Dict: {env_init_result}")

    # # Set the vote for the strategic agent
    env.agents[0].set_vote(
            env.env_vote_scheme,
            env.env_candidates, 
            env.agent_vote_strategy, 
            env_init_result, 
            env.agent_prefs,
            env.agent_votes,
        )
    pprint(f"[Debug]-[Env]- Best vote: {env.agents[0].final_vote} /n Best pref: {env.agents[0].best_pref}")