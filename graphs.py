# Import needed packages
import time
from tqdm import tqdm,tqdm_notebook
import itertools
import numpy as np
import random
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt


class Graph(object):

    def __init__(self,n,m,process_name):
        self.n = int(n)
        self.m = int(m)
        self.n_list = np.linspace(0,self.n-1,self.n).astype(int)
        self.edge_density = m/n
        self.phi = self.edge_density/n
        # tracks edges & orders them by when they were added
        self.edges = np.zeros((n,n),dtype=np.dtype('f4'))
        self.nodes = 0
        self.LJ = 0
        self.process = process_name

    def build(self):
        if self.process=='ER': self.ER()
        elif self.process=='AP': self.AP()
        elif self.process=='DPR': self.DPR()
        else: print('build with a valid process')

    def add_edge(self,edge_tuple):
        # should be non-directed
        if self.edges[edge_tuple[0],edge_tuple[1]]:
            if self.edges[edge_tuple[1],edge_tuple[0]]: pass
            else: print('something is wrong')
        else:
            self.nodes+=1
            self.edges[edge_tuple[0],edge_tuple[1]] = self.nodes
            self.edges[edge_tuple[1],edge_tuple[0]] = self.nodes

    def calculate_node_degrees(self):
        '''
        Calculates the number of connections at each node
        '''
        self.node_degrees = np.copy(np.sum(self.edges>0,axis=1))-1

    def ER(self):
        pbar = tqdm_notebook(total=(self.m-self.nodes),desc="Building standard ER graph")
        while self.nodes<self.m:
            first_node, second_node = random.choice(list(self.n_list)),random.choice(list(self.n_list))
            proposed_edge = tuple((first_node,second_node))
            n0 = self.nodes
            self.add_edge(proposed_edge)
            pbar.update(self.nodes-n0)
        pbar.close()

    def AP(self):
        '''
        The Achlioptas growth process (AP) [16] adds a layer of competition to
        the classical percolation process, whereby edges are ranked
        based on the sizes of the clusters they join and then added
        to the network in such a way as to suppress large cluster growth.
        '''
        return

    def calculate_edge_product(self,edge_tuple):
        return (self.node_degrees[edge_tuple[0]]+1)*(self.node_degrees[edge_tuple[1]]+1)

    def DPR(self):
        '''
        1) A specified number of candidate edges $m$ are chosen uniformly at random
        2) The weight of each candidate edge is calculated as the product of the degrees d of the two
        nodes to be connected by that edge as (d1 + 1)(d2 + 1), where
        one is added to the degree of each node in order to avoid the
        degenerate case of zero-degree nodes.
        3) The edge with the smallest weight is added to the network or, in the case of a tie, an
        edge is chosen at random from the set of edges with the smallest weight
        > in my case, it will not be at random, but will be the first randomly-generated edge with that weight
        '''
        m = 2
        pbar = tqdm_notebook(total=(self.m-self.nodes),desc="Building a degree product rule (DPR) network")
        while self.nodes<self.m:
            # select $m$ candidate edges
            proposed_edges = [(random.choice(list(self.n_list)),random.choice(list(self.n_list))) for i in range(m)]
            self.calculate_node_degrees()
            proposed_edge_weights = [self.calculate_edge_product(edge) for edge in proposed_edges]
            n0 = self.nodes
            self.add_edge(proposed_edges[proposed_edge_weights.index(min(proposed_edge_weights))])
            pbar.update(self.nodes-n0)
        self.calculate_node_degrees()
        print(np.mean(self.node_degrees))
        pbar.close()
