#!/usr/bin/env python

import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import math

bnodes = list(pd.read_csv('path/to/input.csv')['bottom'])
tnodes = list(pd.read_csv('path/to/input.csv')['top'])

# CREATING BIPARTITE NETWORK
def create_bip_network(bnodes,tnodes):

    B = nx.Graph()
    for i in range(len(bnodes)):
        B.add_node(tnodes[i], bipartite=0)
        B.add_node(bnodes[i], bipartite=1)
        B.add_edge(tnodes[i], bnodes[i])

    return B


# CALCULATING COLLABORATIVENESS AND DIVERSITY
def collaborativeness(B):
    
    # splitting the types of nodes of the graph object B
    top_nodes = set(node for node,d in B.nodes(data=True) if d['bipartite']==0) #set of top nodes
    bottom_nodes = set(B) - top_nodes #set of bottom nodes
    deg_top, deg_bottom = bipartite.degrees(B,bottom_nodes) #dictionary: nodes as keys, degrees as values
    
    # creating simple graph and multigraph bottom projections
    G = bipartite.projected_graph(B,bottom_nodes)
    Gm = bipartite.projected_graph(B,bottom_nodes,multigraph=True)
    
    
    col_dict = {} 
    #ratio_dict = {}
    #div_dict = {}
    
    for node in bottom_nodes:
        if G.degree(node) > 0:
            gamma = 0
            shared = 0
            for nbr in B[node]:
                gamma += math.log(B.degree(nbr))
                if B.degree(nbr) > 1:
                    shared += 1
                    
            col_dict[node] = ((float(shared)/B.degree(node))*gamma, float(G.degree(node))/Gm.degree(node))
            #ratio_dict[node] = (float(shared)/B.degree(node))
            #diversity_dict[node] = float(G.degree(node))/Gm.degree(node)
    
    return col_dict

B = create_bip_network(bnodes,tnodes)
col_div = collaborativeness(B)

with open('path/to/output.csv', 'w') as g:
    g.write('node,collaborativeness,diversity')
    g.write('\n')
    for node in list(set(bnodes)):
        g.write(node + ',' + str(col_div[node][0]) + ',' + str(col_div[node][1]))
        g.write('\n')
