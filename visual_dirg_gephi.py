import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
# Load SpaceX's Directed Graph
data = pd.read_csv('data/network_measure_data.csv', index_col = 'Id')
#print(data.columns)
'''
Step 2: Degree distribution histogram [same as networkx]
'''
# Plot degree distribution histogram
degree_seq = sorted(data['Degree'], reverse=True)  
degreeCount = Counter(degree_seq)
deg, count = zip(*degreeCount.items())

fig, ax1 = plt.subplots(figsize=(25,20))
ax1.bar(deg, count, width=1.2, color="b")

plt.title("Degree Distrbution Histogram", fontsize=50, pad=40)
ax1.set_ylabel("Frequency", fontsize=30)
ax1.set_xlabel("Degree", fontsize=30)
ax1.set_xticks(ticks=[0,200,400,600,800,1000])
ax1.set_yticks(ticks=[0,500,1000,1500,2000,2500,3000])
ax1.tick_params(axis='both',labelsize=20)
target_val = float(data['Degree'][data['Label']=='SpaceX'])
for idx, val in enumerate(deg):
    if target_val == val:
        label = 'SpaceX : '+str(target_val)
        ax1.text(val,idx,label,bbox=dict(facecolor='red', alpha=0.4), fontsize=20)
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
ax2.set_ylabel("Frequency", fontsize=15)
ax2.set_xlabel("Degree", fontsize=15)
ax2.set_xticks(ticks=[100,200,400,600,800,1000])
ax2.set_yticks(ticks=[0,2,4])
ax2.tick_params(axis='both',labelsize=12)

ax3 = plt.axes([0.5,0.5,1,1])
ip2 = InsetPosition(ax1, [0.13,0.45,0.5,0.5])
ax3.set_axes_locator(ip2)
mark_inset(ax1, ax3, loc1=2, loc2=4, fc="none", ec='0.5')
ax3.bar(deg[idx+10:-2], count[idx+10:-2], width=0.7, color="b")
ax3.set_ylabel("Frequency", fontsize=15)
ax3.set_xlabel("Degree", fontsize=15)
ax3.set_xticks(ticks=[3,20,40,60,80,100])
ax3.set_yticks(ticks=[0,100,200,300,400])
ax3.tick_params(axis='both',labelsize=12)

plt.show()
#plt.savefig('degree_dist_max_twin_2')

'''
Step 3: Additional network measures
'''
# Network Measure - Clustering Coefficient
try: 
    cl_coef_sorted = data[['Label','clustering']].sort_values(by = ['clustering'], ascending = False)
    cl_coef_sorted = cl_coef_sorted.set_index('Label').T.to_dict('list')
    cl_coef = round(round(data['clustering']/0.05)*0.05,2)
    
    cl_coef_count = Counter(cl_coef)
    coef, coef_count = zip(*cl_coef_count.items())
    plt.figure(figsize=(8,6))
    plt.bar(coef, coef_count,width=0.05,color='b')
    target_val = float(data['clustering'][data['Label']=='SpaceX'])
    for idx, val in enumerate(coef):
        if round(round(target_val/0.05)*0.05,2) == val:
            label = 'SpaceX : '+str(target_val)
            plt.text(val,idx+350,label,bbox=dict(facecolor='red', alpha=0.4), fontsize=10)
            break
    plt.title("Clustering Coefficient Histogram")
    plt.ylabel("Frequency")
    plt.xlabel("Coefficient (round to 0.05)")
    plt.xticks(coef, rotation=45)

    plt.show()
    #plt.savefig('cl_coef_dist')
except:
    cl_coef_sort = None
#print(dict(list(cl_coef_sorted.items())[0:5]))

# Network Measure - Pagarank
try:
    pr_sorted = data[['Label','pageranks']].sort_values(by = ['pageranks'], ascending = False)
    pr_sorted = pr_sorted.set_index('Label').T.to_dict('list')
    pr = round(round(data['pageranks']/0.0005)*0.0005,5)
    pr_counter = Counter(pr)
    pr_counter = dict(sorted(pr_counter.items()))
    prs, pr_count = zip(*pr_counter.items())

    fig, ax1 = plt.subplots(figsize=(15,10))

    plt.title("Pageranks Histogram", fontsize=20, pad=10)
    ax1.bar(prs, pr_count,width=0.0005,color='orange')
    ax1.set_ylabel("Frequency", fontsize=15)
    ax1.set_xlabel("Pagerank (round to 0.0005)", fontsize=15)
    ax1.set_xticks(ticks=np.arange(0,0.0065,0.0005))
    ax1.set_xticklabels(labels=np.arange(0,0.0065,0.0005).round(4),fontsize=12)
    target_val = float(data['pageranks'][data['Label']=='SpaceX'])
    for idx, val in enumerate(prs):
        if round(round(target_val/0.0005)*0.0005,4) == val:
            label = 'SpaceX : '+str(target_val)
            plt.text(val,idx+450,label,bbox=dict(facecolor='red', alpha=0.4), fontsize=12)
            break

    ax2 = plt.axes([0,0,1,1])
    ip = InsetPosition(ax1, [0.4,0.3,0.5,0.5])
    ax2.set_axes_locator(ip)
    mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.0005')

    prs_nozero = prs[1:]
    prs_nozero_count = pr_count[1:]
    ax2.bar(prs_nozero, prs_nozero_count, width=0.0005, color="b")

    xtick = np.arange(0.0005,0.0065,0.0005).round(4)

    ax2_label = [None]*len(xtick)
    for j in range(len(xtick)):
        for i in range(len(prs)-1):
            if prs_nozero[i] == xtick[j]:
                ax2_label[j] = prs_nozero_count[i]

    for idx, val in enumerate(ax2_label):
        if val is not None:
            ax2.text(idx*0.0005+0.00035, val+2, str(val), color='blue')
    ax2.set_ylabel("Frequency", fontsize=10)
    ax2.set_xlabel("Pagerank (round to 0.0005)", fontsize=10)
    ax2.set_xticks(ticks=np.arange(0.0005,0.0065,0.0005).round(4))
    ax2.set_xticklabels(labels=np.arange(0.0005,0.0065,0.0005).round(4),rotation=45)
    ax2.set_yticks(ticks=range(0,350,50))

    plt.show()
    #plt.savefig('pr_dist')
except:
    pr_sorted = None
#print(dict(list(pr_sorted.items())[0:5]))

# Nework Measure - Diameter
try:
    dia = max(data['Eccentricity'])
except:
    dia = None
#print(dia)

# Network Measure - Closeness
try:
    clo_sorted = data[['Label','closnesscentrality']].sort_values(by = ['closnesscentrality'], ascending = False)
    clo_sorted = clo_sorted.set_index('Label').T.to_dict('list')

    clos = round(round(data['closnesscentrality']/0.05)*0.05,2)

    clos_counter = Counter(clos)
    clos_counter = dict(sorted(clos_counter.items()))
    clo, clo_count = zip(*clos_counter.items())

    fig, ax1 = plt.subplots(figsize=(15,10))

    plt.title("Closeness Centrality Histogram", fontsize=20, pad=10)
    ax1.bar(clo, clo_count,width=0.05,color='orange')
    ax1.set_ylabel("Frequency", fontsize=15)
    ax1.set_xlabel("Closeness (round to 0.05)", fontsize=15)
    ax1.set_xticks(ticks=np.arange(0,1.05,0.05))
    target_val = float(data['closnesscentrality'][data['Label']=='SpaceX'])
    for idx, val in enumerate(clo):
        if round(round(target_val/0.05)*0.05,4) == val:
            label = 'SpaceX : '+str(target_val)
            plt.text(val,idx+400,label,bbox=dict(facecolor='red', alpha=0.4), fontsize=12)
            break

    ax2 = plt.axes([0,0,1,1])
    ip = InsetPosition(ax1, [0.4,0.3,0.5,0.5])
    ax2.set_axes_locator(ip)
    mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.0005')

    clo_nozero = clo[1:]
    clo_nozero_count = clo_count[1:]
    ax2.bar(clo_nozero, clo_nozero_count, width=0.05, color="b")

    xtick = np.arange(0.05,1.05,0.05).round(2)

    ax2_label = [None]*len(xtick)
    for j in range(len(xtick)):
        for i in range(len(clo)-1):
            if clo_nozero[i] == xtick[j]:
                ax2_label[j] = clo_nozero_count[i]

    for idx, val in enumerate(ax2_label):
        if val is not None:
            ax2.text(idx*0.05+0.04, val+.5, str(val), color='blue')
    ax2.set_ylabel("Frequency", fontsize=10)
    ax2.set_xlabel("Closeness (round to 0.05)", fontsize=10)
    ax2.set_xticks(ticks=np.arange(0.05,1.05,0.05).round(2))
    ax2.set_xticklabels(labels=np.arange(0.05,1.05,0.05).round(2),rotation=45)
    ax2.set_yticks(ticks=range(0,45,5))

    plt.show()
    #plt.savefig('closeness_dist')
except:
    clo_sorted = None
#print(dict(list(clo_sorted.items())[0:5]))

# Network Measure - Betweenness
try:
    be_sorted = data[['Label','betweenesscentrality']].sort_values(by = ['betweenesscentrality'], ascending = False)
    be_sorted = be_sorted.set_index('Label').T.to_dict('list')
    be = data['betweenesscentrality']
    be = np.log(be[be>0])
    be = round(round(be/0.0005)*0.0005,2)

    be_counter = Counter(be)
    bet, bet_count = zip(*be_counter.items())
    plt.figure(figsize=(12,8))
    plt.bar(bet, bet_count,width=0.05,color='b')
    target_val = np.log(float(data['betweenesscentrality'][data['Label']=='SpaceX']))
    for idx, val in enumerate(bet):
        if round(round(target_val/0.0005)*0.0005,2) == val:
            label = 'SpaceX : '+str(round(target_val,2))
            plt.text(val,idx+1.25,label,bbox=dict(facecolor='red', alpha=0.4), fontsize=12)
            break
    remindertxt = '*96 records only (records with 0.0 betweenness\n centrality are eliminated for better visualization)'
    plt.text(7.6, 3.5,remindertxt,verticalalignment='top',bbox=dict(facecolor='grey', alpha=0.1), fontsize=10)
    plt.title("Betweenness Centrality Histogram*", fontsize=20, pad=10)
    plt.ylabel("Frequency", fontsize=15)
    plt.xlabel("Natural log of Betweenness (round to 0.05)", fontsize=15)
    plt.xticks(ticks=range(0,13,1))
    plt.yticks(ticks=range(0,4,1))
    plt.ylim(0,3.6)

    plt.show()
    #plt.savefig('betweenness_dist')
except:
    be_sorted = None
#print(dict(list(be_sorted.items())[0:5]))

with open('measures_gephi.json','w') as f:
    json.dump({'clustering coef': cl_coef_sorted, 
                'pagerank': pr_sorted, 
                'diameter': dia, 
                'closeness': clo_sorted, 
                'betweenness':be_sorted}, 
                f, indent=4)

