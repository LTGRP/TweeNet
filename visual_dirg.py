import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

with open('data/spacex.json') as file:
    data = json.load(file)

graph = nx.DiGraph()

for node in data:
    adj_list = data[node]
    for adjency in adj_list:
        graph.add_edge(node, adjency['screen_name'])

remove = [node for node, degree in dict(graph.degree()).items() if degree < 2]
graph.remove_nodes_from(remove)
#nx.write_gml(graph, "spacex_di.gml")

# Plot degree distribution histogram
degree_seq = sorted([d for n, d in graph.degree()], reverse=True)  
degreeCount = Counter(degree_seq)
deg, count = zip(*degreeCount.items())

plt.figure(figsize=(25,20))
plt.bar(deg, count, width=1.2, color="b")

plt.title("Degree Distrbution Histogram", fontsize=25)
#plt.ylim(0, 500)
plt.ylabel("Count", fontsize=20)
plt.xlabel("Degree", fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#plt.show()
plt.savefig('degree_dist_max')

# Network Measure - Clustering Coefficient
cl_coef = nx.clustering(graph)
cl_coef_sorted = dict(sorted(cl_coef.items(), key = lambda item:item[1], reverse = True))
#print(dict(list(cl_coef_sorted.items())[0:5]))

# Network Measure - Pagarank
pr = nx.pagerank(graph)
pr_sorted = dict(sorted(pr.items(), key = lambda item:item[1], reverse = True))
#print(dict(list(pr_sorted.items())[0:5]))

# Nework Measure - Diameter
dia = nx.diameter(graph)
#print(dia)

# Network Measure - Closeness
clo = nx.closeness_centrality(graph)
clo_sorted = dict(sorted(clo.items(), key = lambda item:item[1], reverse = True))
#print(dict(list(clo_sorted.items())[0:5]))

# Network Measure - Betweenness
be = nx.betweenness_centrality(graph)
be_sorted = dict(sorted(be.items(), key = lambda item:item[1], reverse = True))
#print(dict(list(be_sorted.items())[0:5]))

with open('measures.json','w') as f:
    json.dump({'clustering coef': cl_coef_sorted, 
                'pagerank': pr_sorted, 
                'diameter': dia, 
                'closeness': clo_sorted, 
                'betweenness':be_sorted}, 
                f, indent=4)


