def test_env():
        # # env_vote_scheme = 'borda'
        # # agent_vote_strategy = 'combination'
        # # num_agents : int = 5, 
        # # num_strat_agents : int = 1,

        # # test define env
        # env = Environment(['c1','c2','c3','c4'], 'borda', 'combination', 'A', 5,1)
        
        # env.collect_prefs_and_votes()
        # print("#"*50)
        # # calculate initial result
        # # pprint(f"Agent preferences: {env.agent_prefs}")
        # # pprint(f"Agent votes: {env.agent_votes}")
        # env_init_result, env_init_result_list = cal_result(env.env_candidates, env.agent_votes)
        # pprint(f"Inital voting result Dict: {env_init_result}\n")
        # # initial happiness
        # env.cal_total_happiness(env_init_result_list)
        # print(f"Initial Total Happiness: {env.total_happiness}\n")

        # # # Set the vote for the strategic agent
        # env.agents[0].set_vote(
        #         env.env_vote_scheme,
        #         env.env_candidates, 
        #         env.agent_vote_strategy,
        #         env.happiness_type, 
        #         env_init_result, 
        #         env.agent_prefs,
        #         env.agent_votes,
        #     )
        # pprint(f"[Debug]-[Env]- Best vote: {env.agents[0].final_vote} /n Best pref: {env.agents[0].best_pref}\n")


        # # collect final votes and preferences
        # env.collect_prefs_and_votes()
        # # calculate final result
        # env_final_result, env_final_result_list = cal_result(env.env_candidates, env.agent_votes)
        # print(f"Final voting result Dict: {env_final_result}")

        # env.cal_total_happiness(env_final_result_list)
        # print(f"Fianl Total Happiness: {env.total_happiness}, Avg. happiness : {env.avg_happiness}")

        ################ 2 agents ####################
        # # test define env
        # print("#"*100)
        # print("#"*100)
        # env = Environment(['c1','c2','c3','c4'], 'borda', 'compromising', 'A', 5,2)   
        # env.collect_prefs_and_votes()
        
        # # calculate initial result
        # # pprint(f"Agent preferences: {env.agent_prefs}")
        # # pprint(f"Agent votes: {env.agent_votes}")
        # env_init_result, env_init_result_list = cal_result(env.env_candidates, env.agent_votes)
        # print(f"Inital voting result Dict: {env_init_result} \n")
        # # store the initial prefs and votes
        # freeze_init_prefs = deepcopy(env.agent_prefs)
        # freeze_init_votes  = deepcopy(env.agent_votes)        
        # # print(f"[Debug]-[Env]- freeze_init_votes: \n ")
        # # pprint(freeze_init_votes)
        # # initial happiness
        # env.cal_total_happiness(env_init_result_list)
        # print(f"Initial Total Happiness: {env.total_happiness} Avg. Happiness: {env.avg_happiness}\n")
        
        
        # print("*"*100)
        # # # Set the vote for the 1st strategic agent
        # env.agents[0].set_vote(
        #         env.env_vote_scheme,
        #         env.env_candidates, 
        #         env.agent_vote_strategy,
        #         env.happiness_type, 
        #         env_init_result, 
        #         freeze_init_prefs,
        #         freeze_init_votes,
        #     )
        # # collect after first voter, votes and preferences
        # env.collect_prefs_and_votes()
        # # calculate final result
        # env_intm_result, env_intm_result_list = cal_result(env.env_candidates, env.agent_votes)
        # print(f"Intermediate voting result Dict: {env_intm_result}")
        # happiness = cal_happiness(env_intm_result_list, env.agents[0].real_preference, env.happiness_type)
        
        # print("*"*100)
        # # # Set the vote for the strategic agent
        # env.agents[1].set_vote(
        #         env.env_vote_scheme,
        #         env.env_candidates, 
        #         env.agent_vote_strategy,
        #         env.happiness_type, 
        #         env_init_result, 
        #         freeze_init_prefs,
        #         freeze_init_votes,
        #     )
        # # collect after first voter, votes and preferences
        # env.collect_prefs_and_votes()
        # # calculate final result
        # env_intm_result, env_intm_result_list = cal_result(env.env_candidates, env.agent_votes)
        # print(f"Intermediate voting result Dict: {env_intm_result}")
        # happiness = cal_happiness(env_intm_result_list, env.agents[0].real_preference, env.happiness_type)
        
        # print("*"*100)
        # print("*"*100)

        # print(f"[Debug]-[Env]- Agent 0 Best vote: {env.agents[0].final_vote} \n Best pref: {env.agents[0].best_pref}\n")
        # print(f"[Debug]-[Env]- Agent 1 Best vote: {env.agents[1].final_vote} \n Best pref: {env.agents[1].best_pref}\n")
        # # collect final votes and preferences
        # env.collect_prefs_and_votes()
        # # calculate final result
        # env_final_result, env_final_result_list = cal_result(env.env_candidates, env.agent_votes)
        # print(f"Final voting result Dict: {env_final_result}")

        # env.cal_total_happiness(env_final_result_list)
        # print(f"Fianl Total Happiness: {env.total_happiness}, Avg. happiness : {env.avg_happiness}")
        ############################# 2/N agents ####################
    pass
        

def max_disatance_sum(num_candidates: int):
    """Calculates the mximum sum of distances for a specific number of canidates.
    It presumes the distance becomes maximum when the two lists are completely inversed. 

    Args:
        num_candidates (int): the number of candidates in result and preference
    """

    n = num_candidates-1
    dist = []
    dist_sum = 0
    if n%2==0:
        # if n is even
        # the distance lists are - 
        # [0], [2,0,2], [4,2,0,2,4]
        for i in range(0,n+2,2):
            dist.append(i)
            dist_sum +=i
    # print(dist,dist_sum)
    else:
        # if n is odd
        # [1,1], [3,1,1,3], [5,3,1,1,3,5]

        for i in range(1,n+2,2):
            dist.append(i)
            dist_sum +=i
    
    # the number repeats twice
    dist_sum*=2
    print(dist,dist_sum)
    return dist_sum

# # Test sum of distances
# num_candidates = [1,2,3,4,5,6,7,8,9,10]
# dist_sums = [max_disatance_sum(i) for i in num_candidates]
# print(f"number of candidates: {num_candidates} \nmaximum_distances: {dist_sums}")

def test_max_distance():
    results = [
        ['c1'],
        ['c1', 'c2'],
        ['c1', 'c2', 'c3'],
        ['c1', 'c2', 'c3', 'c4'],
        # ['c1', 'c2', 'c3', 'c4','c5'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7','c8'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7','c8','c9']
    ]
    max_d = 0

    for r in results:
        print("result", r)
        all_combos = list(set(permutations(r, len(r))))
        for p in all_combos:
            d = abs_pos_distance(r, p)
            d_sum = sum(d)
            if d_sum >= max_d:
                max_d = d_sum
                max_d_p = p
                best_d = d
        # print("result", r)
                print(f"max_d: {max_d}, result: {r}, max_d_pref: {max_d_p}, best_d: {best_d} \n")
        # print(f"length: {len(r)}, max_distance_sum: {max_d}")
def test_cal_happiness(h_type='B'):
    test_list = []
    results = [
        ['c1'],
        ['c1', 'c2'],
        ['c1', 'c2', 'c3'],
        # ['c1', 'c2', 'c3', 'c4'],
        # ['c1', 'c2', 'c3', 'c4','c5'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7','c8'],
        # ['c1', 'c2', 'c3', 'c4','c5','c6','c7','c8','c9']
    ]
    # max_d = 0
    # h_list = []
    for r in results:
        print("result", r)
        all_combos = list(set(permutations(r, len(r))))
        for p in all_combos:
            happiness = cal_happiness(r, p, h_type)
            test_list.append((r,p,happiness))
            # d = abs_pos_distance(r, p)
            # d_sum = sum(d)
            # if d_sum >= max_d:
            #     max_d = d_sum
            #     max_d_p = p
            #     best_d = d
        # print("result", r)
            print(f"preference: {p}, happiness: {happiness} \n")
    return test_list

# test which distribution makes max distance 
    # test_max_distance()
    # Test sum of distances
    # num_candidates = [1,2,3,4,5,6,7,8,9,10]
    # dist_sums = [max_disatance_sum(i) for i in num_candidates]
    # print(f"number of candidates: {num_candidates} \nmaximum_distances: {dist_sums}")
    # test throughly
    # test_list = test_cal_happiness(h_type='B')