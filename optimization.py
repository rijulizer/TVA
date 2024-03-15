import numpy as np
from scipy.optimize import minimize
from utils import cal_happiness, map_vote
from variables import env_candidates, env_vote_scheme

def cost_happiness(weights: np.ndarray, 
                   env_candidates: list = ['c1','c2','c3','c4'],
                   env_result : list = ['c1','c2','c3','c4']):
    
    # order the preference of candidates based on the weights of the candidates
    # more the weight higher the preference
    
    # candidates= ['c1', 'c2', 'c3', 'c4']
    # weights = [w1,      w2,   w3,   w4]
    # instances
    # w0 = [5,     10,   3,  2] # this will be optimized
    # order = [1 0 2 3] 
    # c0 = ['c2' 'c1' 'c3' 'c4']
    order = np.argsort(- weights)
    ordered_pref = np.array(env_candidates)[order]
    happiness = cal_happiness(env_result, ordered_pref)
    return -happiness
    


if __name__ == "__main__":
    candidates=['c1','c2','c3','c4']
    env_result = ['c1','c2','c3','c4']
    preference = np.array(['c1','c2','c3','c4'])
    happiness = cal_happiness(env_result, preference)
    # print(happiness)

    # candidates= ['c1', 'c2', 'c3', 'c4']
    # weights = [w1,      w2,   w3,   w4]
    # weights = [5,     10,   3,  2] # this will be optimized

    # Test:
    # order of indexes based on the values of an array
    # Sample array
    # arr = np.array([5, 10, 3, 2])
    # # Get the order of indices based on the values of arr
    # order = np.argsort(-arr)
    # ordered_pref = preference[order]
    # print(order, ordered_pref)

    # Test cost function 
    weights = np.array([5.0,10.0,3.0,2.0])
    hap = cost_happiness(weights, env_candidates, env_result)
    print(hap)
    # Test optimization
    
    res = minimize(cost_happiness, weights, method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
    print(res)

    print(res.x)