import numpy as np
import matplotlib.pyplot as plt

from clustering import *

def binary_search(graph,start,end,largest_jump,verbose=False):
    ''' Implements binary search to find step at which the largest jump occurs

    Parameters
    ------
    graph : graph object, as defined by graphs.py
    start : starting time step (edge number) of binary search (int)
    end : end time step (edge number) of binary search (int)
    largest_jump : current largest jump (int)
    verbose : used for validating code function (bool)

    Returns
    -----
    largest_jump : size of the largest jump resulting from the addition of one edge (int)

    Note
    -----
    This function is called recursively until the difference in the start and end
    times is only one step.
    '''

    # Define midpoint between provided start and end points
    midpoint = int(round((start+end)/2))

    # Find size of largest SCC at start, midpoint, and end
    head = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=start)))
    mid = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=midpoint)))
    tail = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=end)))

    if verbose:
        print('Edge numbers: %s, %s, %s' %(start,midpoint,end))
        print('Largest SCC: %s, %s, %s' %(head,mid,tail))

    # If start and end are only one step removed from on another, then search is complete
    if abs(end-start)==1:
        if (tail-head)>largest_jump: largest_jump = (tail-head)
        return largest_jump
    # Check which side of the midpoint the largest jump is on
    elif (mid-head)>(tail-mid):
        if (mid-head)>(graph.n/100):
            largest_jump = (mid-head)
            return binary_search(graph,start,midpoint,largest_jump, verbose)
    elif (tail-mid)>(graph.n/100):
        largest_jump = (tail-mid)
        return binary_search(graph,midpoint,end,largest_jump, verbose)
    return largest_jump

def get_largest_jump(graph,verbose=False):
    ''' Finds the largest jump resulting from the addition of one edge

    Parameters
    ------
    graph : graph object, as defined by graphs.py
    verbose :

    Returns
    -----
    jump : size of the largest jump resulting from the addition of one edge (int)
    '''

    # Set initial bounds for the binary search
    start = 1
    end = graph.m-1

    # Find size of largest SCC at start and end
    head = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=start)))
    tail = ranked_SCC(tarjan((graph.edges>0)*(graph.edges<=end)))

    largest_jump = 0
    if (tail-head)<(graph.n/100): jump = (tail-head)
    else: jump = binary_search(graph,start,end,largest_jump,verbose)
    return int(jump)
