import numpy as np
from variables import env_candidates, env_vote_scheme
# distances
def abs_pos_distance(list_o, list_p):
    """
    Calculate the absolute positional distance between two lists of equal length.

    Parameters:
    - list_o (list): The outcome of the voting
    - list_b (list): The preference list.

    Returns:
    list: The list of distances 
    """
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

# voting schemes
def voting_scheme(env_vote_scheme: str, agent_prefs: dict) -> list[str]:
    """
    calculates the result of voting/preferences based on the voting scheme 
    Parameters:
    - env_vote_scheme (str): type of voting scheme
    Returns:
    (list): voting preferences
    """

    # Borda voting
    inital_result = {}
    if env_vote_scheme == 'borda':
        for pref in agent_prefs.values():
            # calculate borda value of the preference list
            borda_val = np.array(range(len(pref)-1,-1,-1))
            for c, v in zip(pref, borda_val):
                if c in inital_result.keys():
                    inital_result[c] += v
                else:
                    inital_result[c] = v
        # Sort the dictionary by values in reverse order
        #TODO: if two candidates have the result then order alphabatically             
        sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict
            

if __name__ == "__main__":
    # Test        
    # Example usage:
    o = ['c1', 'c2', 'c3', 'c4']
    p = ['c4', 'c2', 'c1', 'c3']

    distance = abs_pos_distance(o, p)
    # print(f"The distance between lists o and p is: {distance}")

    x= 1/(1+np.array(distance))
    # print("X:", x, np.ones_like(x), np.dot(x, np.ones_like(x)))
    # print("X:", x, [0.5,0.5,0,0], np.dot(x, np.array([0.5,0.5,0,0])))
    # print(np.array(range(len(p)-1,-1,-1)))

    inital_result = {}
    # if env_vote_scheme == 'borda':
    # pref = ['c1', 'c2', 'c3', 'c4']
    agent_prefs = {'a1': ['c1', 'c2', 'c3', 'c4'],
                   'a2': ['c1', 'c2', 'c3', 'c4'],
                   'a3': ['c4', 'c2', 'c1', 'c3']}
    for pref in agent_prefs.values():
        # calculate borda value of the preference list
        borda_val = np.array(range(len(pref)-1,-1,-1))
        for c, v in zip(pref, borda_val):
            if c in inital_result.keys():
                inital_result[c] += v
            else:
                inital_result[c] = v
    # Sort the dictionary by values in reverse order
    sorted_dict = dict(sorted(inital_result.items(), key=lambda item: item[1], reverse=True))

    # Print the sorted dictionary
    print(inital_result)
    print(sorted_dict)