import json
import networkx as nx

with open('./data/spacex.json') as file:
    data = json.load(file)

graph = nx.DiGraph()

for node in data:
    adj_list = data[node]
    for adjency in adj_list:
        graph.add_edge(node, adjency['screen_name'])

remove = [node for node, degree in dict(graph.degree()).items() if degree < 2]
graph.remove_nodes_from(remove)
nx.write_gml(graph, "./gml/spacex_di.gml")
