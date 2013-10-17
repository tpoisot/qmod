#!/usr/bin/python2

import networkx as nx
import scipy as sp
import numpy as np
import random

## data

G = nx.DiGraph()
# Two loops with a link between them
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(3, 2, weight=1)
G.add_edge(1, 4, weight=0.01)
G.add_edge(4, 5, weight=1)
G.add_edge(4, 6, weight=1)
G.add_edge(5, 6, weight=1)
G.add_edge(6, 4, weight=1)

## Weigthed modularity
def Qq(G):
   Qq = 0.0
   sum_of_links = np.sum([e['weight'] for e in G.edges])
   return Qq

## weigthed pick function
def wsample(d):
  # need a dict {'value': weight}
  r = random.uniform(0, sum(d.itervalues()))
  s = 0.0
  for k, w in d.iteritems():
    s+= w
    if r < s : return k
  return k

## label propagation function
def qlp(G):
  optim = []
  # We first initialize the labels
  labid = {}
  for n in G:
    labid[n] = n
  nx.set_node_attributes(G, 'label', labid)
  optim.append([G.node[n]['label'] for n in G])
  # Now we can start a number of iterations
  for i in xrange(100):
    # The nodes propagate their labels in a random order
    updateorder = range(G.number_of_nodes())
    random.shuffle(updateorder)
    for updated in updateorder:
      # First we pick the outgoing edges
      out_edges = G.edges([updated], data=True)
      if len(out_edges) > 0:
	pick_prob = {}
	for out_e in out_edges:
	  pick_prob[out_e[1]] = out_e[2]['weight']
	# We pick at random according to the weight
	receiver = wsample(pick_prob)
	G.node[receiver]['label'] = G.node[updated]['label']
    optim.append([G.node[n]['label'] for n in G])
  return optim

print qlp(G)

