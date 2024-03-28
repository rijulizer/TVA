import numpy as np
from agent import Agent
from utils import map_vote, cal_result, cal_happiness
from pprint import pprint

class Environment:
    def __init__(
        self,
        env_candidates : list[str] = ['c1','c2','c3','c4'], 
        env_vote_scheme: str = 'borda', 
        agent_vote_strategy : str = 'compromising', #['compromising', 'bullet_voting', 'combination']
        happiness_type : str = 'A', #B, #C
        num_agents : int = 5, 
        num_strat_agents : int = 1,
        ):
        
        self.env_candidates = env_candidates
        self.env_vote_scheme = env_vote_scheme 
        self.agent_vote_strategy = agent_vote_strategy
        self.num_agents = num_agents
        self.num_strat_agents = num_strat_agents
        self.happiness_type = happiness_type
        
        self.agents = []
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = 0
        self.total_risk = 0
        self.avg_happiness = 0
        
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
            if agent.strategy:
                pprint(f"[DEBUG]-[Env]- Agent: {agent.name}, strategic_agent: {agent.strategy}, preference: {agent.real_preference}\n")
        
    def collect_prefs_and_votes(self):
        """
        Collects the preferences and votes of all the agents in the env
        """
        for a in self.agents:
            
            # if the agent has a best preference then get that otherwise get real preference 
            if len(a.best_pref)!=0:
                self.agent_prefs[a.name] = a.best_pref
            else:
                # get preferences
                self.agent_prefs[a.name] = a.real_preference
            # get votes
            # if the agent has a final vote then get that instead of getting vote from preference 
            if len(a.final_vote)!=0:
                # only for startegic agents
                self.agent_votes[a.name] = a.final_vote
            else:
                self.agent_votes[a.name] = map_vote(self.env_vote_scheme, self.env_candidates, a.real_preference)
        print(f"[DEBUG]-[Env], votes: {self.agent_votes} \n")
   
    def cal_total_happiness(self, env_result_list):
        """Calculates the total happiness of the system
        """
        self.total_happiness = 0
        for a in self.agents:
            hap_init = cal_happiness(env_result_list, self.agent_prefs[a.name], self.happiness_type)
            self.total_happiness += hap_init
        self.avg_happiness = round(self.total_happiness/len(self.agents), 2)

        return self.total_happiness, self.avg_happiness

    def calculate_risk(self,env_result_list):
        no_candidates = len(env_result_list.keys())
        no_buckets = no_candidates -1
        alpha_risk = np.ones(no_buckets)
        total_votes = list(env_result_list.values())
        difference = [(total_votes[i-1] - total_votes[i]) for i in range(1,no_candidates,1)]
        self.total_risk = np.round(1/(1+np.sum(np.array(difference)*alpha_risk)/no_buckets),3)
        print(f"[DEBUG]-[Env] calculate_risk total_votes:{total_votes}")
        return self.total_risk
    
    def calculate_final_risk(self):
        env_final_result, _ = cal_result(self.env_candidates, self.agent_votes)
        return self.calculate_risk(env_final_result)

if __name__ == "__main__":
    # env_vote_scheme = 'borda'
    # agent_vote_strategy = 'combination'
    # num_agents : int = 5, 
    # num_strat_agents : int = 1,

    # test define env
    env = Environment(['c1','c2','c3','c4'], 'borda', 'combination', 'A', 5,1)
    
    env.collect_prefs_and_votes()
    print("#"*50)
    # calculate initial result
    # pprint(f"Agent preferences: {env.agent_prefs}")
    # pprint(f"Agent votes: {env.agent_votes}")
    env_init_result, env_init_result_list = cal_result(env.env_candidates, env.agent_votes)
    pprint(f"Inital voting result Dict: {env_init_result}\n")
    # initial happiness
    env.cal_total_happiness(env_init_result_list)
    print(f"Initial Total Happiness: {env.total_happiness}\n")

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
    pprint(f"[Debug]-[Env]- Best vote: {env.agents[0].final_vote} /n Best pref: {env.agents[0].best_pref}\n")


    # collect final votes and preferences
    env.collect_prefs_and_votes()
    # calculate final result
    env_final_result, env_final_result_list = cal_result(env.env_candidates, env.agent_votes)
    print(f"Final voting result Dict: {env_final_result}")

    env.cal_total_happiness(env_final_result_list)
    print(f"Final Total Happiness: {env.total_happiness}, Avg. happiness : {env.avg_happiness}")

    risk = env.calculate_final_risk()
    print(f"Final Total Risk: {risk}")
