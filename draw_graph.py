import networkx as nx
from matplotlib import pyplot as plt

from cbs_net import Net
# from cbs_net import Stochastic
# from cbs_net import Route

n = Net()
n.load_from_file('rynek.txt')

min_x, max_x = 100, 0
min_y, max_y = 100, 0

f = open('rynek_nodes.txt', 'r')
for data_line in f:
    data = data_line.split('\t')
    nd = n.get_node(int(data[0]))
    nd.name = str(data[1])
    nd.x = float(data[2])
    nd.y = float(data[3])
    if nd.x < min_x: min_x = nd.x
    if nd.y < min_y: min_y = nd.y
    if nd.x > max_x: max_x = nd.x
    if nd.y > max_y: max_y = nd.y
f.close()

print min_x, max_x, min_y, max_y
# normalize coordinates
for nd in n.nodes:
    nd.x = (nd.x - min_x) / (max_x - min_x)
    nd.y = (nd.y - min_y) / (max_y - min_y)


G = nx.Graph()
for nd in n.nodes:
    G.add_node(nd.code, pos=(nd.y, nd.x))
for lnk in n.links:
    G.add_edge(lnk.out_node.code, lnk.in_node.code)

pos = nx.get_node_attributes(G, 'pos')
# print pos

nx.draw(G, pos, with_labels=True, font_size=8, alfa=0.5)
plt.show()
