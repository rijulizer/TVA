import numpy as np
from agent import Agent
from utils import map_vote, cal_result
from happiness import cal_happiness
from pprint import pprint
from copy import deepcopy
import randomname
import argparse
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
        print("\n\n")
        print("#"*100)
        print("#"*100)
        print(f"Creating Enviroment: {randomname.get_name()}")
        
        self.env_candidates = env_candidates
        self.env_vote_scheme = env_vote_scheme 
        self.agent_vote_strategy = agent_vote_strategy
        self.num_agents = num_agents
        self.num_strat_agents = num_strat_agents
        self.happiness_type = happiness_type
        self.strategy_occured = False
        
        self.agents = []
        self.agent_prefs = {}
        self.agent_votes = {}
        self.total_happiness = 0
        self.total_risk = 0
        self.avg_happiness = 0

        
        print(f"[Env]-[Params]:, \ncandidates: {env_candidates}, \nvoting scheme: {env_vote_scheme},\nagent_vote_strategy: {agent_vote_strategy},\nhappiness_type: {happiness_type}, \nnum_agents: {num_agents}, \nnum_strat_agents: {num_strat_agents}")
        print("#"*100)
        
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
                print(f"[DEBUG]-[Env]- Agent: {agent.name}, strategic_agent: {agent.strategy}, preference: {agent.real_preference}\n")

        
        
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
            if a.strategy_occured:
                self.strategy_occured = True
        print(f"[DEBUG]-[Env]- votes: \n")
        pprint(self.agent_votes)
   
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

    def run_tva(self):
        """runs a round of voting
            Step-0: Create environment
            Step-1: Get all agents preferences and votes
            Step-2: Calculate inital result
            Step-3: Stategic agent sets votes
            step-4: Calculate final result
        
        """
        
        print(f"[Debug]-[run_tva]-Runing a voting process... \n")
        # Collect initial preferences and votes 
        self.collect_prefs_and_votes()
        # calculate initial result
        env_init_result, env_init_result_list = cal_result(self.env_candidates, self.agent_votes)
        print(f"Inital voting result Dict: {env_init_result} \n")
        # store the initial prefs and votes as this would chaneg for multiple startegic voter
        freeze_init_prefs = deepcopy(self.agent_prefs)
        freeze_init_votes  = deepcopy(self.agent_votes)        
        # print(f"[Debug]-[Env]- freeze_init_votes: \n ")
        # pprint(freeze_init_votes)

        # calculate initial happiness
        self.cal_total_happiness(env_init_result_list)
        print(f"Initial Total Happiness: {self.total_happiness} \n")
        
        # strategic agents giving votes
        print("*"*100)
        for i in range(self.num_strat_agents):
            print(f"Startegic agent {i} is giving vote \n")
            # for each strategic agent, set the vote strategically based on inital results 
            # and their knowledge of other agents preferneces and votes
            self.agents[i].set_vote(
                    self.env_vote_scheme,
                    self.env_candidates, 
                    self.agent_vote_strategy,
                    self.happiness_type, 
                    env_init_result, 
                    freeze_init_prefs,
                    freeze_init_votes,
                )
            if self.num_strat_agents >=2:
                # [Debug] The next section is only needed for debugging
                # collect votes and preferences, after each startegic voter this modifes the agent votes 
                self.collect_prefs_and_votes()
                # calculate intermediate result
                env_intm_result, env_intm_result_list = cal_result(self.env_candidates, self.agent_votes)
                print(f"Intermediate voting result Dict: {env_intm_result}")
                self.cal_total_happiness(env_intm_result_list)
                print(f"Intermediate Total Happiness: {self.total_happiness} \n")
                # agent_happiness = cal_happiness(env_intm_result_list, env.agents[i].real_preference, self.happiness_type)
                print("*"*100)

        # Final calculations
        print("*"*100)

        # collect final votes and preferences
        self.collect_prefs_and_votes()
        # calculate final result
        env_final_result, env_final_result_list = cal_result(self.env_candidates, self.agent_votes)
        print(f"Final voting result Dict: {env_final_result}")

        self.cal_total_happiness(env_final_result_list)
        print(f"Fianl Total Happiness: {self.total_happiness}")
        
        # Calcualte risk
        final_total_risk = self.calculate_final_risk()
        print(f"Fianl Total Risk: {final_total_risk}")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Creates a single voting environment with agents doing voting for candidates"
                                    )
    parser.add_argument("--candidates",
                        dest='env_candidates',
                        default=['c1','c2','c3','c4'],
                        nargs='+',
                        type=str,
                        help="List of canidates to vote for (default: ['c1','c2','c3','c4'])"
                        )

    parser.add_argument("--scheme",
                        dest='env_vote_scheme',
                        default="borda",
                        choices=["plurality", "anti_plurality", "voting_for_two","borda"],
                        help="Voting scheme used for counting votes (default: borda)",
                        )

    parser.add_argument("--strategy",
                        dest='agent_vote_strategy',
                        default="compromising",
                        choices=['compromising', 'bullet_voting', 'combination'],
                        help="Strategy used by agent to manipulate vote (default: compromising)")
    
    parser.add_argument("--hppiness_type",
                        dest='happiness_type',
                        default="A",
                        choices=['A', 'B', 'C'],
                        help="Types of happiness function (default: A)")

    parser.add_argument("--num_agents",
                        dest='num_agents',
                        default=5,
                        type=int,
                        help="Total number of agents including strategic agents  (default: 5)")

    parser.add_argument("--num_strat_agents",
                        dest='num_strat_agents',
                        default=1,
                        type=int,
                        help="Number of strategic agents  (default: 1)")

    args = parser.parse_args()

    env_candidates = args.env_candidates
    env_vote_scheme = args.env_vote_scheme
    agent_vote_strategy = args.agent_vote_strategy
    happiness_type = args.happiness_type
    num_agents = args.num_agents
    num_strat_agents = args.num_strat_agents
    env = Environment(
        env_candidates, 
        env_vote_scheme, 
        agent_vote_strategy, 
        happiness_type, 
        num_agents, 
        num_strat_agents
    )
    env.run_tva()
    risk = env.calculate_final_risk()
 
# running instruction            
#    --candidates 'c1' 'c2' 'c3' 'c4' --scheme 'borda' --strategy 'compromising' --num_agents 5 --num_strat_agents 2
