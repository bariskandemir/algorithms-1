# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 22:16:54 2016

Assignment 3- Random Contraction Algorithm

@author: bzk142
"""
"""
Download the following text file:

kargerMinCut.txt
The file contains the adjacency list representation of a simple undirected graph. There are 200 vertices labeled 1 to 200. 
The first column in the file represents the vertex label, and the particular row (other entries except the first column) tells 
all the vertices that the vertex is adjacent to. So for example, the 6th row looks like : "6	155	56	52	120	......". 
This just means that the vertex with label 6 is adjacent to (i.e., shares an edge with) the vertices 
with labels 155,56,52,120,......,etc

Your task is to code up and run the randomized contraction algorithm for the min cut problem and use it on the above graph 
to compute the min cut. (HINT: Note that you'll have to figure out an implementation of edge contractions. 
Initially, you might want to do this naively, creating a new graph from the old every time there's an edge contraction. 
But you should also think about more efficient implementations.) (WARNING: As per the video lectures, please make sure 
to run the algorithm many times with different random seeds, and remember the smallest cut that you ever find.) 
Write your numeric answer in the space provided. So e.g., if your answer is 5, just type 5 in the space provided.
"""

import numpy as np
import random
import time
import pandas
from collections import Counter



def PopulateGraph(filestr):
    f = open(filestr, "r")

    graph = {}
    for line in f:
        temp_line = line.rstrip('\n').split(' ')

        for i in range(0,len(temp_line)):
            graph[temp_line[0]] = temp_line[1:len(temp_line)]
    return graph;
    
def RandomContract(graph):
    

    random.seed(time.clock()*100)
    temp_key = random.choice(graph.keys())
    neighbors = np.asarray(graph[temp_key])
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

    
def CountVertices(graph):
    return len(graph.keys())

def ReadjustEdges(graph, newKey, temp_key, temp_neigh):
    neighbors = graph[newKey];
    for i in neighbors:
        temp_neighs = graph[i];

        tempi = np.where(np.asarray(temp_neighs) == temp_key)
        if len(tempi[0])!=0:
            for n in tempi[0]:            
                temp_neighs[n] = newKey;
        
        tempi = np.where(np.asarray(temp_neighs) == temp_neigh)
        if len(tempi[0])!=0:
            for m in tempi[0]:
                temp_neighs[m] = newKey;
        graph[i] = temp_neighs;

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



cuts_l = [[] for _ in range(1000)];
for t in range(0,1000):
    
    mygraph = PopulateGraph('kargerMinCut.txt')
    copy_g = PopulateGraph('kargerMinCut.txt');
    while (CountVertices(copy_g)>2):
        copy_g = RandomContract(copy_g);

    zika = FindCuts(copy_g, mygraph)
    print(zika)
    cuts_l[t].extend(zika)

minik = 9999
for im in cuts_l:
    if len(im)<minik:
        minik = len(im);
print(minik)
