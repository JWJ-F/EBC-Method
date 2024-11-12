import networkx as nx
import glob
import os
import copy
import pandas as pd
from math import sqrt
import sys



# ==============圈基====================
def attack_cycles_for_edge(graph):

    # 计算每条边参与的圈基数量
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

    # 按照参与圈基数量从大到小排序
    sorted_edges = sorted(edge_cycle_counts.items(), key=lambda x: x[1], reverse=True)

    # data_list = []
    # for edge, _ in sorted_edges:
    #     graph.remove_edge(*edge)
    #     largest_component = len(max(nx.connected_components(graph), key=len))
    #     rate = float(largest_component) / max_component
    #     data_list.append(rate)
    #
    # return data_list

    data_list = robustnessEdges(graph, sorted_edges)
    return data_list


def robustnessEdges(graph, sorted_edges):
    max_component = float(graph.number_of_nodes())
    data_list = []

    for edge, _ in sorted_edges:
        graph.remove_edge(*edge)
        largest_component = len(max(nx.connected_components(graph), key=len))
        rate = float(largest_component) / max_component
        data_list.append(rate)

    return data_list

def readTxt2(filename):

    edges = []

    f = open(filename, 'r')
    for row in f:
        i = row.rstrip()
        i = i.split(' ')
        edge = []
        for ii in i:
            if ii != '':
                ii = int(ii)
                edge.append(ii)
        edges.append(edge)

    f.close()

    return edges

def readCSV2(csv_file_path):

    data = pd.read_csv(csv_file_path)

    # 将前两列数据添加为图的边
    edges = zip(data.iloc[:, 0], data.iloc[:, 1])

    return edges

def saveTxt1(count_list, OutputAddress):
    with open(OutputAddress, 'w+') as f:
            for num in count_list:
                data = str(num) + "\n"
                # print(data)
                f.writelines(data)

def saveTxtRobustness(outputRobustnessAddress, dataStr):
    # 打开文件以追加内容
    with open(outputRobustnessAddress, 'a') as file:
        # 写入新的内容
        file.write(dataStr+'\n')

def readNet(filename):
    # edges = readTxt2(filename)
    edges = readCSV2(filename)
    G = nx.Graph()
    # G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    # i = 0
    # for edge in edges:
    #     print(i)
    #     i=i+1
    #     G.add_edge(*edge)
    return G

def iterAttack(G0, file_name, outputRobustnessAddress, outputAddress):
    data_list =[]
    for i in range(8):
        G1 = copy.deepcopy(G0)
        newOutputAddress = outputAddress + pointer_name[i] + '\\' + file_name + "_attack.txt"
        newOutputRobustnessAddress = outputRobustnessAddress + pointer_name[i] + "_robustness.txt"
        if i == 0:# 圈基
            data_list = attack_cycles_for_edge(G1)

        robustness = sum(data_list) / len(data_list)
        saveTxt1(data_list, newOutputAddress)
        print(f"--{newOutputAddress}")

        dataStr = file_name + " " + str(robustness)

        saveTxtRobustness(newOutputRobustnessAddress, dataStr)



# main
# inputAddress = r'E:\code\python\edgesAttack\data3\networks\cycles\*.txt'
inputAddress = r'E:\code\python\edgesAttack\data3\networks\cycles\a\*.csv'
outputAddress = r'E:\code\python\edgesAttack\data3\attack\cycles\\'
outputRobustnessAddress = r'E:\code\python\edgesAttack\data3\robustness\cycles\\'
pointer_name = ['cycles_for_edge']



txt_files = glob.glob(inputAddress)
# files = []
for i in range(len(txt_files)):#  len(txt_files)  #

    txt_file = txt_files[i]
    G0 = readNet(txt_file)
    # 去除不联通的分支
    node_num = float(G0.number_of_nodes())
    largest_component = max(nx.connected_components(G0), key=len)
    if len(largest_component) < node_num:
        G0 = G0.subgraph(largest_component).copy()
    # 去除自环
    G0.remove_edges_from(nx.selfloop_edges(G0))
    file_name = os.path.basename(txt_file.split('.')[0])

    print(f"({i})============{file_name}:开始")
    iterAttack(G0, file_name, outputRobustnessAddress, outputAddress)
    # files.append(file_name)

    print(f"============{file_name}:结束")
    print("=======================================")





