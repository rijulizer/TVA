import numpy as np
# voting schemes deprecated
def voting_scheme(env_vote_scheme: str, agent_prefs: dict) -> list[str]:

#     """
#     calculates the result of voting/preferences based on the voting scheme 
#     Parameters:
#     - env_vote_scheme (str): type of voting scheme
#     Returns:
#     (dict): candidates with their votes in the order from highest to lowest
#     (list): list of candidates in the order from highest to lowest
#     """
#     inital_result = {}
#     for c in env_candidates:
#         inital_result[c]=0
#     # Borda voting
    
#     if env_vote_scheme == 'borda':
#         for pref in agent_prefs.values():
#             # calculate borda value of the preference list
#             borda_val = np.array(range(len(pref)-1,-1,-1))
#             for c, v in zip(pref, borda_val):
#                 if c in inital_result.keys():
#                     inital_result[c] += v
#                 else:
#                     inital_result[c] = v
#         # Sort the dictionary by values in reverse order
#         #TODO: if two candidates have the result then order alphabatically             
#         sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
#         sorted_list = list(sorted(inital_result, key=inital_result.get, reverse=True))

#     # Plurality / Voting for one 
    
#     if env_vote_scheme == 'plurality':
#         for pref in agent_prefs.values():
#             # retrieve the first vote from the preference list
#             if pref[0] in inital_result.keys():
#                 inital_result[pref[0]] += 1
#             else:
#                 inital_result[pref[0]] = 1
#         sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
#         sorted_list = list(sorted(inital_result, key=inital_result.get, reverse=True))

#     #TODO: if the candidate has no votes manually add it in the result with 0 votes 
#     #Example- {'c4': 3, 'c2': 1, 'c3': 1}" should be {'c4': 3, 'c2': 1, 'c3': 1, 'c1': 0}"
#     # voting for two
    
#     if env_vote_scheme == 'voting_for_two':
#         for pref in agent_prefs.values():
#             # retrieve the first two votes from the preference list
#             for j in range(2):
#                 if pref[j] in inital_result.keys():
#                     inital_result[pref[j]] += 1
#                 else:
#                     inital_result[pref[j]] = 1
#         sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
#         sorted_list = list(sorted(inital_result, key=inital_result.get, reverse=True))

#     # anti plurality voting
    
#     if env_vote_scheme == 'anti_plurality_voting':
#         for pref in agent_prefs.values():
#             # retrieve all the votes except from the last one from the preference list
#             for j in range(len(pref)):
#                 if j!= len(pref)-1:
#                     if pref[j] in inital_result.keys():
#                         inital_result[pref[j]] += 1
#                     else:
#                         inital_result[pref[j]] = 1
#         sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
#         sorted_list = list(sorted(inital_result, key=inital_result.get, reverse=True))

#     return sorted_dict, sorted_list
    pass

# voting schemes
def map_vote(env_vote_scheme: str, env_candidates: list[str], pref: list[str], bullet_voting: bool = False) -> list[int]:
    """maps the prefernce of a single agent to a vote based on the voring scheme

    Args:
        env_vote_scheme (str): 
        env_candidates (list[str]): 
        pref (list[str]): the list of candidate preference of an agent
        bullet_voting (bool, optional): whether bullet voting or not. Defaults to False.

    Returns:
        list[int]: _description_
    """
    # TODO: implement the bullet_voting logic
    if env_vote_scheme == 'plurality':
        # check with all the elements of env_candidates with the first preference
        vote = np.array(env_candidates)==pref[0]
        vote = vote.astype(int)
        
    elif env_vote_scheme == 'anti_plurality':
        # check with all the elements of env_candidates with the last preference
        vote = np.array(env_candidates) != pref[-1]
        vote = vote.astype(int)
        
    elif env_vote_scheme == 'voting_for_two':
        vote = np.logical_or(np.array(env_candidates) == pref[0], np.array(env_candidates) == pref[1])
        vote = vote.astype(int)
        
    elif env_vote_scheme == 'borda':

        vote = [len(env_candidates)-pref.index(c)-1 for c in env_candidates]
        # vote = [len(env_candidates)-pref.index(c)-1 for c in env_candidates]

    
    else:
        raise ValueError("env_vote_scheme should be on of the options")

    # print(f"[Debug]-[utils]-[map_vote]- pref : {pref}, vote: {vote}")

    # if bullet voting the vote is always the highest preference only! 1 for antiplurality and voting for two, len(vote)-1 for borda
    if bullet_voting:

        vote = np.array(env_candidates)==pref[0]
        vote = vote.astype(int)
        if env_vote_scheme == 'borda':
            vote *= (len(vote)-1)
    return vote

def cal_result(env_candidates, votes: dict) -> (dict,list) : #-> tuple[dict,list]
    inital_result = {}
    # iterate all the agent votes
    for vote in votes.values():
        # iterates all the candidates
        for c_index, c_val in enumerate(env_candidates):
            # check if the candidate is a key in the inital_result
            if c_val in inital_result.keys():
                # add the vote of the candidate
                inital_result[c_val] += vote[c_index]
            else:
                inital_result[c_val] = vote[c_index]
    
    # sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))
    # Sort based on the reverse of values and alphabatical order of keys
    sorted_dict = dict(sorted(inital_result.items(), key=lambda item:(-item[1],item[0])))
    sorted_list = list(sorted(sorted_dict, key=inital_result.get, reverse=True))
    return (sorted_dict, sorted_list)

if __name__ == "__main__":
    # Test        
    # Example usage:
    # o = ['c1', 'c2', 'c3', 'c4']
    # p = ['c4', 'c2', 'c1', 'c3']

    # distance = abs_pos_distance(o, p)
    # # print(f"The distance between lists o and p is: {distance}")

    # x= 1/(1+np.array(distance))
    # # print("X:", x, np.ones_like(x), np.dot(x, np.ones_like(x)))
    # # print("X:", x, [0.5,0.5,0,0], np.dot(x, np.array([0.5,0.5,0,0])))
    # # print(np.array(range(len(p)-1,-1,-1)))

    # inital_result = {}
    # # if env_vote_scheme == 'borda':
    # # pref = ['c1', 'c2', 'c3', 'c4']
    # agent_prefs = {'a1': ['c1', 'c2', 'c3', 'c4'],
    #                'a2': ['c1', 'c2', 'c3', 'c4'],
    #                'a3': ['c4', 'c2', 'c1', 'c3']}
    # for pref in agent_prefs.values():
    #     # calculate borda value of the preference list
    #     borda_val = np.array(range(len(pref)-1,-1,-1))
    #     for c, v in zip(pref, borda_val):
    #         if c in inital_result.keys():
    #             inital_result[c] += v
    #         else:
    #             inital_result[c] = v
    # # Sort the dictionary by values in reverse order
    # sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))

    # # Print the sorted dictionary
    # print(inital_result)
    # print(sorted_dict)

    # test plurality
    env_candidates
    p = ['c4', 'c2', 'c1', 'c3']
    vote = np.array(env_candidates)==p[0]
    vote = vote.astype(int)
    print(f"[Debug]-[utils]-pref : {p}, vote: {vote}")

    # test anti_plurality_voting
    env_candidates
    p = ['c4', 'c2', 'c1', 'c3']
    vote = np.array(env_candidates) != p[-1]
    vote = vote.astype(int)
    print(f"[Debug]-[utils]-pref : {p}, vote: {vote}")

    # test vote for 2 
    env_candidates
    p = ['c4', 'c2', 'c1', 'c3']
    vote = np.logical_or(np.array(env_candidates) == p[0], np.array(env_candidates) == p[1])
    vote = vote.astype(int)
    print(f"[Debug]-[utils]-pref : {p}, vote: {vote}")

    # test borda
    positions = [len(env_candidates)-p.index(c)-1 for c in env_candidates]
    print(positions)