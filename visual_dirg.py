import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
# Load SpaceX's Directed Graph 
graph = nx.read_gml('gml/spacex.gml')

'''
Step 2: Degree distribution histogram
'''
# Plot degree distribution histogram
degree_seq = sorted([d for n, d in graph.degree()], reverse=True)  
degreeCount = Counter(degree_seq)
deg, count = zip(*degreeCount.items())

fig, ax1 = plt.subplots(figsize=(25,20))
ax1.bar(deg, count, width=1.2, color="b")

plt.title("Degree Distrbution Histogram", fontsize=50, pad=40)
ax1.set_ylabel("Count", fontsize=30)
ax1.set_xlabel("Degree", fontsize=30)
ax1.set_xticks(ticks=[0,200,400,600,800,1000])
ax1.set_yticks(ticks=[0,500,1000,1500,2000,2500,3000])
ax1.tick_params(axis='both',labelsize=20)
for n, d in graph.degree():
    for idx, val in enumerate(deg):
        if n == 'SpaceX' and d == val:
            label = n+': '+str(d)
            ax1.text(val,idx,n+': '+str(d),bbox=dict(facecolor='red', alpha=0.4), fontsize=20)
            break

ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax1, [0.6,0.1,0.3,0.3])
ax2.set_axes_locator(ip)
mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')
idx = 0
for i in range(len(deg)):
    if deg[i] <= 150 :
        idx = i
        break
ax2.bar(deg[:idx], count[:idx], width=1.2, color="b")
ax2.set_ylabel("Count", fontsize=15)
ax2.set_xlabel("Degree", fontsize=15)
ax2.set_xticks(ticks=[100,200,400,600,800,1000])
ax2.set_yticks(ticks=[0,2,4])
ax2.tick_params(axis='both',labelsize=12)

ax3 = plt.axes([0.5,0.5,1,1])
ip2 = InsetPosition(ax1, [0.13,0.45,0.5,0.5])
ax3.set_axes_locator(ip2)
mark_inset(ax1, ax3, loc1=2, loc2=4, fc="none", ec='0.5')
ax3.bar(deg[idx+10:-2], count[idx+10:-2], width=0.7, color="b")
ax3.set_ylabel("Count", fontsize=15)
ax3.set_xlabel("Degree", fontsize=15)
ax3.set_xticks(ticks=[3,20,40,60,80,100])
ax3.set_yticks(ticks=[0,100,200,300,400])
ax3.tick_params(axis='both',labelsize=12)

#plt.show()
plt.savefig('degree_dist_max_twin_2')

'''
Step 3: Additional network measures
'''
# Network Measure - Clustering Coefficient
try: 
    cl_coef = nx.clustering(graph)
    cl_coef_sorted = dict(sorted(cl_coef.items(), key = lambda item:item[1], reverse = True))
except:
    cl_coef_sort = None
#print(dict(list(cl_coef_sorted.items())[0:5]))

# Network Measure - Pagarank
try:
    pr = nx.pagerank(graph)
    pr_sorted = dict(sorted(pr.items(), key = lambda item:item[1], reverse = True))
except:
    pr_sorted = None
#print(dict(list(pr_sorted.items())[0:5]))

# Nework Measure - Diameter
try:
    dia = nx.diameter(graph)
except:
    dia = None
#print(dia)

# Network Measure - Closeness
try:
    clo = nx.closeness_centrality(graph)
    clo_sorted = dict(sorted(clo.items(), key = lambda item:item[1], reverse = True))
except:
    clo_sorted = None
#print(dict(list(clo_sorted.items())[0:5]))

# Network Measure - Betweenness
try:
    be = nx.betweenness_centrality(graph)
    be_sorted = dict(sorted(be.items(), key = lambda item:item[1], reverse = True))
except:
    be_sorted = None
#print(dict(list(be_sorted.items())[0:5]))

with open('measures_un.json','w') as f:
    json.dump({'clustering coef': cl_coef_sorted, 
                'pagerank': pr_sorted, 
                'diameter': dia, 
                'closeness': clo_sorted, 
                'betweenness':be_sorted}, 
                f, indent=4)
