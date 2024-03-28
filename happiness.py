import numpy as np
from itertools import permutations
# distances used for happiness calculation
def abs_pos_distance(list_o, list_p):
    """
    Calculate the absolute positional distance between two lists of equal length.

    Parameters:
    - list_o (list): The outcome of the voting
    - list_b (list): The preference list.

    Returns:
    list: The list of distances 
    """
    assert len(list_o)==len(list_p) , "size of output and preference should be same"
    dict_o = {}
    dist = []
    # convert the list to a dict where the key is the element of the list and 
    # value i sthe index of the element
    for i in range(len(list_o)):
        dict_o[list_o[i]] = i
    # Calculate the positional distances
    for i in range(len(list_p)):
        dist.append(abs(dict_o[list_p[i]] - i))
    return dist

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

def cal_happiness(env_result: list, pref: list, type: str = 'A'):
    """
    Calculates agents individual happiness
    Parameters:
    - env_result (list): The voting result from environment
    - pref (list): The agents prefernce order for the candidates
    Returns:
    hapiness (float)
    """

    if type == 'A':
        ## Beauty Contest
        # calculate the distance
        raw_distances = abs_pos_distance(env_result, pref)
        # max sum of distances in the worst cases for scaling
        worst_dist_sum = max_disatance_sum(len(env_result))
        scaled_distances = np.round(np.array(raw_distances)/ worst_dist_sum,3)
        # get total disatnces
        total_distance = np.sum(scaled_distances)
        happiness = 1 - total_distance
        
    elif type == 'B':
        ## Shareholder/Greek-election
        # calculate the distance
        raw_distances = abs_pos_distance(env_result, pref)
        # max sum of distances in the worst cases for scaling
        worst_dist_sum = max_disatance_sum(len(env_result))
        scaled_distances = np.round(np.array(raw_distances)/ worst_dist_sum,3)
        # alpha assigns weights to each index as a priority
        # linearly decreasing weights
        alpha = np.array([i for i in range(len(env_result), 0, -1)])
        alpha = alpha * len(env_result) / np.sum(alpha) # scale alpha
        # total distanced is weighted with alpha
        total_distance = np.round(np.dot(alpha,scaled_distances),3)
        # for some cases the distance can become more than 1, limit it to 1
        total_distance = min(total_distance, 1)
        happiness = 1-total_distance
        
    elif type == 'C':
        beta = [pow(0.5,i) for i in range(len(pref))]
        beta[-1] = 0
        happiness = beta[pref.index(env_result[0])]
    else:
        raise NotImplementedError("Not a valid happiness function")

        
    # print(f"[DEBUG]-[cal_happiness] raw_distances: {raw_distances}")
    # print(f"[DEBUG]-[cal_happiness] scaled_distances: {scaled_distances}")
    # print(f"[DEBUG]-[cal_happiness]- alpha: {alpha}")
    # print(f"[DEBUG]-[cal_happiness]- total_distance: {total_distance}")
    # self.happiness = happiness
    return happiness
        
    
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
# calculate happiness
# def cal_happiness(env_result: list, pref: list, type: str):
#     """
#     Calculates agents individual happiness
#     Parameters:
#     - env_result (list): The voting result from environment
#     - pref (list): The agents prefernce order for the candidates
#     Returns:
#     hapiness (float)
#     """

#     if type == 'A':
#         # calculate the distance
#         raw_distances = abs_pos_distance(env_result, pref)
#         # print(f"[DEBUG]-[cal_happiness] raw_distances: {raw_distances}")
#         x = 1/(1+np.array(raw_distances))
#         # print(f"[DEBUG]-[cal_happiness] x: {x}")
#         alpha = np.ones_like(x)
#         # print(f"[DEBUG]-[cal_happiness]- alpha: {alpha}")
#         # happiness
#         happiness = np.round(np.dot(alpha,x)/ np.sum(alpha),3)
#         # self.happiness = happiness
#     elif type == 'B':
#         # calculate the distance
#         raw_distances = abs_pos_distance(env_result, pref)
#         # print(f"[DEBUG]-[cal_happiness] raw_distances: {raw_distances}")
#         x = 1/(1+np.array(raw_distances))
#         # print(f"[DEBUG]-[cal_happiness] x: {x}")
#         # TODO Change this to something that works with any number of candidates
#         alpha = [0.5, 0.2, 0.15, 0.1, 0.05]
#         # print(f"[DEBUG]-[cal_happiness]- alpha: {alpha}")
#         # happiness
#         happiness = np.round(np.dot(alpha,x)/ np.sum(alpha),3)
#         # self.happiness = happiness
#     elif type == 'C':
#         beta = [pow(0.5,i) for i in range(len(pref))]
#         beta[-1] = 0
#         happiness = beta[pref.index(env_result[0])]
#     else:
#         raise NotImplementedError("Not a valid happiness function")
#     return happiness

if __name__ == "__main__":
    
    # test which distribution makes max distance 
    # test_max_distance()
    # Test sum of distances
    # num_candidates = [1,2,3,4,5,6,7,8,9,10]
    # dist_sums = [max_disatance_sum(i) for i in num_candidates]
    # print(f"number of candidates: {num_candidates} \nmaximum_distances: {dist_sums}")

    # # test calculate happiness
    cal_happiness(['c1', 'c2', 'c3'], ['c2', 'c1','c3'], 'B')
    cal_happiness(['c1', 'c2','c3', 'c4'], ['c2', 'c1','c3','c4'])
    # test throughly
    test_list = test_cal_happiness(h_type='B')