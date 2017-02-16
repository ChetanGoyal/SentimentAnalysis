"""
cluster.py
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math


def buildingGraph():
    tv_graph = nx.Graph()
    with open('tweeting_user.txt') as tweeting_users:
        for edge in tweeting_users:
            nodes = edge.strip('\n').split(',')
            tv_graph.add_edge(nodes[0], nodes[1])
    summary = open('summary.txt', 'a')
    summary.write("The number of edges " + str(tv_graph.number_of_edges()) + "\n")
    summary.write("The number of nodes " + str(tv_graph.number_of_nodes()) + "\n")
    summary.close()

    nx.draw(tv_graph, cmap=plt.get_cmap('jet'))
    # plt.show()
    return tv_graph


def Girvan_newman(tv_graph, depth):
    if tv_graph.order() == 1:
        return [tv_graph.nodes()]

    def find_best_edge(G0):
        eb = nx.edge_betweenness_centrality(G0)
        return sorted(eb.items(), key=lambda x: x[1], reverse=True)[0][0]

    components = [c for c in nx.connected_component_subgraphs(tv_graph)]
    indent = '   ' * depth
    while len(components) == 1:
        edge_to_remove = find_best_edge(tv_graph)
        # print(indent + 'removing ' + str(edge_to_remove))
        tv_graph.remove_edge(*edge_to_remove)
        components = [c for c in nx.connected_component_subgraphs(tv_graph)]

    result = [c.nodes() for c in components]
    # print(indent + 'components=' + str(result))
    for c in components:
        result.extend(Girvan_newman(c, depth + 1))

    return result


clusters = Girvan_newman(buildingGraph(), 1)
summary = open('summary.txt', 'a')
summary.write("The number of clusters created " + str(len(clusters)) + "\n")
nodes_per_cluster = 0
for i in clusters:
    nodes_per_cluster = nodes_per_cluster + len(i)

summary.write("The average number of nodes in a cluster " + str(math.ceil(nodes_per_cluster / len(clusters))) + "\n")
summary.close()
print("Successful")