# Import needed packages
import time
from tqdm import tqdm,tqdm_notebook
import itertools
import numpy as np
import random
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

G = nx.Graph()

class WorkingGraph(object):

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
        G = nx.Graph()
        G.add_nodes_from(np.arange(self.n))
        while self.nodes<self.m:
            first_node, second_node = random.choice(list(self.n_list)),random.choice(list(self.n_list))
            proposed_edge = tuple((first_node,second_node))
            n0 = self.nodes
            self.add_edge(proposed_edge)
            pbar.update(self.nodes-n0)
        pbar.close()
