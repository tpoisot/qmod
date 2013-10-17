#!/usr/bin/python2

import networkx as nx
import scipy as sp
import numpy as np
import random
import matplotlib.pyplot as plt
import sys

## Data
mat = np.loadtxt('q.txt')
G = nx.from_numpy_matrix(mat, create_using = nx.DiGraph())

## Delta function
def delta(a, b):
   if a == b:
      return 1
   return 0

## Weigthed modularity
def Qq(G):
   Qq = 0.0
   sum_of_links = np.sum([e[2]['weight'] for e in G.edges(data=True)])
   for up in G.nodes(data=True):
      for down in G.nodes(data=True):
         c1 = up[1]
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
  # We print the first modularity value
  print Qq(G)
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
