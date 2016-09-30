# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:16:54 2016

Assignment 3- Random Contraction Algorithm

@author: bzk142
"""
import numpy as np
import random
import time
import pandas
from collections import Counter

def PopulateGraph(filestr):
    f = open(filestr, "r")
#    num_lines = sum(1 for line in open('myfile.txt'))
    graph = {}
    for line in f:
        temp_line = line.rstrip('\n').split(' ')
#        temp_line = line[0:len(line)];
#        temp_line_lst = temp_line.split(' ')
#        temp_lst = np.asarray(temp_line);
#        temp_lst = [map(int, x) for x in temp_lst]
        for i in range(0,len(temp_line)):
            graph[temp_line[0]] = temp_line[1:len(temp_line)]
    return graph;
    
def RandomContract(graph):
    
#    key_list = graph.keys()
#    ind_key = random.sample(range(0, len(key_list)),  1)
    random.seed(time.clock()*100)
    temp_key = random.choice(graph.keys())
    neighbors = np.asarray(graph[temp_key])
#    neigh_ind = random.sample(range(0,len(neighbors)), 1)
    random.seed(time.clock()*101)
    temp_neigh = random.choice(neighbors)
    
    temp_neigh_n = np.asarray(graph[temp_neigh]);
    tempin = np.where(neighbors != temp_neigh)
    if len(tempin[0]) !=0:
        nehgbors_clnd = list(neighbors[tempin[0]])
    else:
        nehgbors_clnd = []
    tempin = np.where(temp_neigh_n != temp_key)
    if len(tempin[0]) !=0:
        temp_neigh_n_clnd = list(temp_neigh_n[tempin[0]])
    else:
        temp_neigh_n_clnd = []
#    nehgbors_clnd = neighbors[np.where(neighbors != temp_neigh)]
#    temp_neigh_n_clnd = temp_neigh_n[np.where(temp_neigh_n!=temp_key)]
    union = list(set(nehgbors_clnd)|set(temp_neigh_n_clnd));
    newKey = ','.join([temp_key, temp_neigh])
    if newKey in graph:
        graph[newKey].append(union)
    else:
        graph[newKey] = union
    del graph[temp_key]
    del graph[temp_neigh]
    graph = ReadjustEdges(graph, newKey, temp_key, temp_neigh);
    return graph
#    ind_list = graph[key_list[ind_key]]
    
def CountVertices(graph):
    return len(graph.keys())

def ReadjustEdges(graph, newKey, temp_key, temp_neigh):
    neighbors = graph[newKey];
    for i in neighbors:
        temp_neighs = graph[i];
#        temp_neighs = array(str(temp_neighs), '|S3')
        tempi = np.where(np.asarray(temp_neighs) == temp_key)
        if len(tempi[0])!=0:
            for n in tempi[0]:            
                temp_neighs[n] = newKey;
        
        tempi = np.where(np.asarray(temp_neighs) == temp_neigh)
        if len(tempi[0])!=0:
            for m in tempi[0]:
                temp_neighs[m] = newKey;
        graph[i] = temp_neighs;
#        graph[i].append(np.asarray(newKey))
    return graph
        
def FindCuts(graph, orig_g):
    keyz = graph.keys()
    cuts = [];
    for k in keyz:
        key_elements = k.split(',')
        neighs = graph[k]
        n_key_elements = neighs[0].split(',')
        for e in key_elements:
            orig_neigh = orig_g[e]
            intersect = list(set(orig_neigh)&set(n_key_elements))
            for z in range(0, len(intersect)):
                cuts.append([e, intersect[z]])
        break
    return cuts;
"""
-------------------------------------------------------------
"""


#random.seed(1000)
cuts_l = [[] for _ in range(1000)];
for t in range(0,1000):
    
    mygraph = PopulateGraph('kargerMinCut.txt')
    copy_g = PopulateGraph('kargerMinCut.txt');
    while (CountVertices(copy_g)>2):
        copy_g = RandomContract(copy_g);
#    print(copy_g)
    zika = FindCuts(copy_g, mygraph)
    print(zika)
    cuts_l[t].extend(zika)

minik = 9999
for im in cuts_l:
    if len(im)<minik:
        minik = len(im);
print(minik)
