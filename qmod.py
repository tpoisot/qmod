#!/usr/bin/python2

import networkx as nx
import scipy as sp
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
import json

## Data
def prepareData(fname):
   mat = np.abs(np.loadtxt(fname))
   G = nx.from_numpy_matrix(mat, create_using = nx.DiGraph())
   return G

## Delta function
def delta(a, b):
   if a == b:
      return 1
   return 0

## Weigthed modularity
def Qq(G):
   Qq = 0.0
   sum_of_links = np.sum([e[2]['weight'] for e in G.edges(data=True)])
   marginals = []
   for l in G.edges(data=True):
      n1 = G.node[l[0]]
      n2 = G.node[l[1]]
      if delta(n1['label'], n2['label']) == 0:
         marginals.append(0)
      else :
         w_l = l[2]['weight']
         suc = G.successors(l[0])
         pre = G.predecessors(l[1])
         w_i = np.sum([G[l[0]][s]['weight'] for s in suc])
         w_j = np.sum([G[p][l[1]]['weight'] for p in pre])
         marginals.append(w_l/float(sum_of_links) - (w_i*w_l)/float(sum_of_links**2.0))
   return np.sum(marginals)

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
def qlp(G,steps=100):
   optim = {}
   # We first initialize the labels
   labid = {}
   for n in G:
      labid[n] = n
   nx.set_node_attributes(G, 'label', labid)
   # We print the first modularity value
   optim["0"]={'Q':Qq(G),'labels':{str(n):G.node[n]['label'] for n in G}}
   # Now we can start a number of iterations
   for i in xrange(steps):
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
      optim[str(i)]={'Q':Qq(G),'labels':{str(n):G.node[n]['label'] for n in G}}
   return optim

def pickBestPartition(run):
   # Returns the best partition (i.e. higher modularity score)
   best_partition = {}
   best_q = 0.0
   for k in run.keys():
      if run[k]['Q'] > best_q:
         best_partition = run[k]
   return best_partition
         

def speciesImpactByRemoval(G, steps):
   Impact = {}
   for n in G.nodes():
      tG = G.copy()
      tG.remove_node(n)
      Out = qlp(tG, steps)
      Impact[str(n)] = pickBestPartition(Out)
   return Impact

def analyzeFile(fname, steps):
   G = prepareData(fname)
   mod = qlp(G, steps)
   ## Analyse modularity
   out = open(fname+'.json', 'w')
   out.write(json.dumps(mod, out, sort_keys=True))
   out.close()
   best_partition = pickBestPartition(mod)
   out = open(fname+'.best.json', 'w')
   out.write(json.dumps(best_partiton, out, sort_keys=True))
   out.close()
   ## Test species impact by removal
   sp_imp_rem = speciesImpactByRemoval(G, steps)
   out = open(fname+'.rem.json', 'w')
   out.write(json.dumps(sp_imp_rem, out, sort_keys=True))
   out.close()
   return 0

if __name__ == "__main__":
   #TODO Need to add an help in case the args are mot O.K.
   # Read arguments
   prefix = str(sys.argv[1])
   steps = int(sys.argv[2])
   # Read binary file
   analyzeFile(prefix+'.bnr', steps)
   # Read quantitative prefix
   analyzeFile(prefix+'.qnt', steps)
