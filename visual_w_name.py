#!/usr/bin/env python
# coding: utf-8

get_ipython().run_line_magic('matplotlib', 'inline')

import json
import matplotlib.pyplot as plt
import networkx as nx


with open('an_hsuan.json') as file:
    data = json.load(file)

target = data['an_hsuan'][1]
friends = data['NASA']

ids = [i['id'] for i in data['NASA']]
accounts = [target['id']]+ids

# Initialize network graph
graph = nx.Graph()

# Add nodes of all Twitter accounts
graph.add_nodes_from(accounts)

# Add edges between nodes and node detials
for friend in friends:
    graph.add_edge(target['id'], friend['id'])
    graph.nodes[target['id']]['screen_name'] = target['screen_name']
    graph.nodes[friend['id']]['screen_name'] = friend['screen_name']
    
# Create a dict for mapping labels
mapping = {target['id']:target['screen_name']}
for friend in friends:
    mapping.update({friend['id']:friend['screen_name']})

# Plot the network graph
plt.figure(figsize=(15,10))

# Code to set the position of labels slightly off the node
pos_orig=nx.spring_layout(graph)
pos_higher = {}
x_off = 0.05
y_off = 0.08 

for k, v in pos_orig.items():
    if (v[1]>0.5):
        pos_higher[k] = (v[0], v[1]+y_off)
    else:
        pos_higher[k] = (v[0], v[1]-y_off)

# Draw one layer without label for positioning label on the next layer
nx.draw_networkx(graph, pos = pos_orig, with_labels = False)
nx.draw_networkx_labels(graph, pos = pos_higher, labels = mapping)
plt.axis("off")
plt.show(block=False)

#plt.savefig('NASA_v1')
