#!/usr/bin/env python
# coding: utf-8

get_ipython().run_line_magic('matplotlib', 'inline')

import json
import matplotlib.pyplot as plt
import networkx as nx

with open('data.json') as file2:
    data2 = json.load(file2)

prim_ac_list = list(data2.keys())

"""
Create Undirected Graph with all friends
"""

ac_list = []
for i in range(len(prim_ac_list)):
    ac_list.append(int(prim_ac_list[i]))
    ac_list.extend(data2[prim_ac_list[i]])
    
#len(ac_list)

graph2 = nx.Graph()

graph2.add_nodes_from(ac_list)
for account in data2:
    for i in range(len(data2[account])):
        graph2.add_edge(account, data2[account][i])

remove = [node for node,degree in dict(graph2.degree()).items() if degree < 2]
graph2.remove_nodes_from(remove)


plt.figure(figsize=(25,20))
d = graph2.degree()
nx.draw(graph2, with_labels = False, node_size=[v * 100 for k,v in d])
#nx.draw_networkx_labels(graph, pos = pos_higher, labels = mapping)
plt.axis("off")
plt.show(block=False)

#plt.savefig('NASA_v3')

"""
Create Undirected Graph with the first 20 friends
"""

ac_list2 = []
for i in range(20):
    ac_list2.append(int(prim_ac_list[i]))
    ac_list2.extend(data2[prim_ac_list[i]])
    
#len(ac_list2)

graph3 = nx.Graph()

graph3.add_nodes_from(ac_list2)
acs = [prim_ac_list[i] for i in range(20)]
for account in acs:
    for i in range(len(data2[account])):
        graph3.add_edge(account, data2[account][i])


remove2 = [node for node,degree in dict(graph3.degree()).items() if degree < 2]
graph3.remove_nodes_from(remove2)


plt.figure(figsize=(25,20))
d = graph3.degree()
nx.draw(graph3, with_labels = False, node_size=[v * 100 for k,v in d])
#nx.draw_networkx_labels(graph, pos = pos_higher, labels = mapping)
plt.axis("off")
plt.show(block=False)

#plt.savefig('NASA_v4')

