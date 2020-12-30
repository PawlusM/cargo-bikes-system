import networkx as nx
# import graphviz
from matplotlib import pyplot as plt

from cbs_net import Net

# from cbs_net import Stochastic
# from cbs_net import Route

n = Net()
n.load_from_file('rynek_links.txt')

min_x, max_x = 100, 0
min_y, max_y = 100, 0

f = open('rynek_nodes.txt', 'r')
for data_line in f:
    data = data_line.split('\t')
    nd = n.get_node(int(data[0]))
    nd.name = str(data[1])
    nd.x = float(data[3])
    nd.y = float(data[4])
    if str(data[2]) == 'R':
        nd.type = 'restaurant'
    elif str(data[2]) == 'H':
        nd.type = 'hotel'
    elif str(data[2]) == 'B':
        nd.type = 'bar'
    elif str(data[2]) == 'K':
        nd.type = 'cafe'
    elif str(data[2]) == 'S':
        nd.type = 'shop'
    elif str(data[2]) == 'Ks':
        nd.type = 'bookstore'
    elif str(data[2]) == 'L':
        nd.type = 'loadpoint'
    if nd.x < min_x: min_x = nd.x
    if nd.y < min_y: min_y = nd.y
    if nd.x > max_x: max_x = nd.x
    if nd.y > max_y: max_y = nd.y
f.close()

# print min_x, max_x, min_y, max_y
# normalize coordinates
for nd in n.nodes:
    nd.x = (nd.x - min_x) / (max_x - min_x)
    nd.y = (nd.y - min_y) / (max_y - min_y)
    # print nd.type

G = nx.Graph()
for nd in n.nodes:
    G.add_node(nd.code, pos=(nd.y, nd.x))
for lnk in n.links:
    G.add_edge(lnk.out_node.code, lnk.in_node.code)

pos = nx.get_node_attributes(G, 'pos')
color_map = {'restaurant': 'darkblue',
             'cafe': 'blue',
             'bar': 'purple',
             'hotel': 'red',
             'shop': 'grey',
             'bookstore': 'green',
             'loadpoint': 'orange'
             # 'notype': 'white'
             }
colors = [color_map.get(nd.type) for nd in n.nodes]
# print pos

# for nd in n.nodes:
#     dn = nx.draw_networkx_nodes(G, pos=pos, alpha=0.5, nodelist=[nd.code], node_color='green')

# nx.draw_networkx(G, pos=pos, with_labels=True, font_size=8, alpha=0.5)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for label in color_map:
    ax.scatter([], [], color=color_map[label], label=label)

nx.draw_networkx_nodes(G, pos=pos,
                       nodelist=range(730),
                       alpha=0.6,
                       node_color=colors, ax=ax, node_size=200)

nx.draw_networkx_nodes(G, pos=pos,
                       nodelist=range(730),
                       alpha=0.6,
                       node_color=colors, ax=ax, node_size=200)
nx.draw_networkx_nodes(G, pos=pos,
                       nodelist=range(730, 736),
                       alpha=1.0,
                       node_color="orange", ax=ax, node_size=300)

nx.draw_networkx_edges(G, pos=pos, style='dotted')

G = nx.relabel_nodes(G, mapping={730: 'A', 731: 'B', 732: 'C',
                                 733: 'D', 734: 'E', 735: 'F'}, copy=False)
pos['A'] = pos[730]
pos['B'] = pos[731]
pos['C'] = pos[732]
pos['D'] = pos[733]
pos['E'] = pos[734]
pos['F'] = pos[735]
lp_codes = ['A', 'B', 'C', 'D', 'E', 'F']
loadpoints = {}
for nd in G.nodes():
    if nd in lp_codes:
        loadpoints[nd] = nd

nx.draw_networkx_labels(G, pos, loadpoints, ax=ax)

plt.axis('off')
plt.legend(loc='lower right', fontsize='large')
fig.tight_layout()
plt.show()
