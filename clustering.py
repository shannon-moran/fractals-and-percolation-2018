import random
import itertools

import numpy as np
import matplotlib.pyplot as plt

def matrix_to_tuples(adjacency_matrix):
    ''' Converts adjacency matrix to list of edge tuples for ease of viewing
    '''
    edge_locations=np.where(adjacency_matrix>0)
    edges = []
    for i in range(len(edge_locations[0])):
        edges.append((edge_locations[0][i]+1,edge_locations[1][i]+1))
    return sorted(edges)

def ranked_SCC(SCCs,rank=1):
    ''' Sorts SCCs by number of nodes

    By default, pulls the largest SCC, but `rank` can be used to pull second largest,
    third largest, etc. This includes a safety exist if rank > number of SCCs.
    '''
    C = sorted(SCCs,key=len,reverse=True)
    if rank>len(C): return 0
    else: return len(C[rank-1])

def tarjan(edges):
    ''' Use Tarjan's Algorithm to find all strongly connected components in graph

    Parameters
    -----
    edges : (nxn) numpy array
        Adjacency matrix containing all tail-head edge pairs in a graph

    Returns
    -----
    component_list : list of tuples
        Each SCC is contained in a tuple, which is then stored as a list element

    Reference
    ------
    [1] Depth-first search and linear graph algorithms, R. Tarjan
       SIAM Journal of Computing 1(2):146-160, (1972).
    '''

    # Store order of first visit (index) and oldest ancestor (lowlink) for each node
    index = {}
    lowlink = {}

    # Keep track of discovery "time"
    visit_index = [0]

    stack = []
    component_list = []

    def visit_children(node):
        # Only run for the first time a node is visited
        # Updates discovery time and ancestor
        index[node] = visit_index[0]
        lowlink[node] = visit_index[0] # Will be updated further in function
        visit_index[0] += 1

        stack.append(node)

        # Collect all nodes (heads) a given node is tail to (from adjacency matrix)
        try: children = np.where(edges[node]!=0)[0]
        except: children = []

        # Repeat DFS for each child of a node
        for child in children:
            # If the child hasn't been visited, recursively run search
            if child not in lowlink:
                visit_children(child)
                lowlink[node] = min(lowlink[node],lowlink[child])
            # If the child is in the stack, that means they're also in the SCC
            # Update the lowest accesible ancestor
            elif child in stack:
                lowlink[node] = min(lowlink[node],index[child])

        # If the visit time and lowest ancestor of a node are the same,
        # the SCC includes the entire stack down to the root node.
        # Pop off the stack and store it in the component_list as a tuple.
        if lowlink[node]==index[node]:
            SCC = []
            while True:
                successor = stack.pop()
                SCC.append(successor)
                if successor == node: break
            component_list.append(tuple(SCC))

    # Ensures algorithm visits each node
    for node in range(edges.shape[0]):
        if node not in lowlink:
            visit_children(node)

    return component_list
