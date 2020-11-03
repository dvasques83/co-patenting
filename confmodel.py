"""

This script creates a configuration model for
bipartite networks

    Return a bipartite graph with configuration model
    (keeping degree sequence of both sets of nodes but rewiring links)

    Parameters
    aseq: degree sequence of top nodes
    bseq: degree sequence of bottom nodes
           
Author: Demi Vasques

"""

import networkx as nx
from networkx.algorithms import bipartite
import random
import time

def conf_model(aseq, bseq):
    
    t0 = time.time()
    
    G=nx.empty_graph(0,create_using=nx.Graph())
    
    # length and sum of each sequence
    lena=len(aseq)
    lenb=len(bseq)
    suma=sum(aseq)
    sumb=sum(bseq)

    if not suma==sumb:
        raise networkx.NetworkXError(\
              'invalid degree sequences, sum(aseq)!=sum(bseq),%s,%s'\
              %(suma,sumb))

    G.add_nodes_from(range(lena),bipartite=0)
    G.add_nodes_from(range(lena,lena+lenb,1),bipartite=1)
                       
    if max(aseq)==0: return G  # done if no edges

    # build lists of degree-repeated vertex numbers
    stubs=[]
    stubs.extend([[v]*aseq[v] for v in range(0,lena)])  
    astubs=[]
    astubs=[x for subseq in stubs for x in subseq]

    stubs=[]
    stubs.extend([[v]*bseq[v-lena] for v in range(lena,lena+lenb)])  
    bstubs=[]
    bstubs=[x for subseq in stubs for x in subseq]

    # shuffle lists
    random.shuffle(astubs)
    random.shuffle(bstubs)
    
    while astubs:
        source = astubs.pop()
        target = bstubs.pop()
            
        G.add_edge(source,target)

    #G.add_edges_from([[astubs[i],bstubs[i]] for i in range(suma)])

    #G.name="bipartite_configuration_model"
    
    print 'Running time to create config model network: ' + str(time.time() - t0)
    
    return G
