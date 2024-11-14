import networkx as nx
import glob
import os
import copy
import pandas as pd
from math import sqrt
import sys

def EBC(graph):
    # Calculate the number of cycles that each edge participates in
    edge_cycle_counts = {}
    for edge in graph.edges():
        edge_cycle_counts[edge] = 0

    cycle_bases = nx.cycle_basis(graph)
    for cycle in cycle_bases:
        for i in range(len(cycle)):
            edge1 = (cycle[i - 1], cycle[i])
            edge2 = (cycle[i], cycle[i - 1])
            if edge1 in edge_cycle_counts.keys():
                edge_cycle_counts[edge1] = edge_cycle_counts[edge1] + 1
            elif edge2 in edge_cycle_counts.keys():
                edge_cycle_counts[edge2] = edge_cycle_counts[edge2] + 1

    # Order the number of participating cycles from largest to smallest
    sorted_edges = sorted(edge_cycle_counts.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_edges


def edge_attack_robustness(graph, sorted_edges):
    max_component = float(graph.number_of_nodes())
    data_list = []
    
    data_list.append(1.0) 

    for edge, _ in sorted_edges:
        graph.remove_edge(*edge)
        largest_component = len(max(nx.connected_components(graph), key=len))
        rate = float(largest_component) / max_component
        data_list.append(rate)
    
    robustness = sum(data_list) / len(data_list)

    return data_list,robustness 


# main
g = nx.Graph()
EBC_edge = EBC(g)
LCC_curve,R_e = edge_attack_robustness(g, EBC_edge)



