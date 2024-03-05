import numpy as np
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

if __name__ == "__main__":
    # Test        
    # Example usage:
    o = ['c1', 'c2', 'c3', 'c4']
    p = ['c4', 'c2', 'c1', 'c3']

    distance = abs_pos_distance(o, p)
    print(f"The distance between lists o and p is: {distance}")

    x= 1/(1+np.array(distance))
    print("X:", x, np.ones_like(x), np.dot(x, np.ones_like(x)))
    # print("X:", x, [0.5,0.5,0,0], np.dot(x, np.array([0.5,0.5,0,0])))
