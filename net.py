import random
import numpy as np

import stochastic
import link
import node
import consignment


class Net:
    """ Delivery network as the graph model """

    def __init__(self):
        # network model time
        self.time = 0
        # duration of the network simulation [min]
        self.duration = 0
        # network geography
        self.nodes = []
        self.links = []
        # transport demand
        self.demand = []

    def contains_node(self, node_code):
        """" Determines if the network contains a node with the specified code """
        for n in self.nodes:
            if n.code == node_code:
                return True
        return False

    def get_node(self, code):
        """" Returns the first found node with the specified code """
        for n in self.nodes:
            if n.code == code:
                return n
        return None

    def contains_link(self, out_node, in_node):
        """ Checks if the net contains a link """
        for l in self.links:
            if l.out_node is out_node and l.in_node is in_node:
                return True
        return False

    def get_link(self, out_node, in_node):
        """" Returns the first found link with the specified out and in nodes """
        for lnk in self.links:
            if lnk.out_node is out_node and lnk.in_node is in_node:
                return lnk
        return None

    def add_link(self, out_code, in_code, weight=0, directed=False):
        """" Adds a link with the specified characteristics """
        if self.contains_node(out_code):
            # out-node is already in the net
            out_node = self.get_node(out_code)
            if self.contains_node(in_code):
                # in-node is already in the net
                in_node = self.get_node(in_code)
                if self.contains_link(out_node, in_node):
                    # out-node and in-node are already linked: change the link weight
                    self.get_link(out_node, in_node).weight = weight
                else:
                    # there is no such a link in the net: add a new one
                    new_link = link.Link(out_node, in_node, weight)
                    out_node.out_links.append(new_link)
                    in_node.in_links.append(new_link)
                    self.links.append(new_link)
            else:
                # the net contains the specified out-node, but there is no in-node with the specified code
                in_node = node.Node(in_code)
                new_link = link.Link(out_node, in_node, weight)
                out_node.out_links.append(new_link)
                in_node.in_links.append(new_link)
                self.nodes.append(in_node)
                self.links.append(new_link)
        else:
            # the net does not contain the specified out-node
            out_node = node.Node(out_code)
            if self.contains_node(in_code):
                # in-node is already in the net
                in_node = self.get_node(in_code)
            else:
                # there are no in-node and out-node with the specified codes
                in_node = node.Node(in_code)
                self.nodes.append(in_node)
            # create new link
            new_link = link.Link(out_node, in_node, weight)
            out_node.out_links.append(new_link)
            in_node.in_links.append(new_link)
            self.nodes.append(out_node)
            self.links.append(new_link)
        # add the reverse link
        if not directed:
            self.add_link(in_code, out_code, weight, True)
        # sort the nodes (is useful for calculating the short distances matrix)
        # self.nodes.sort()

    @property
    def to_matrix(self):
        max_code = max([n.code for n in self.nodes])
        mtx = [[float('inf') for __ in range(max_code + 1)]
               for _ in range(max_code + 1)]
        for lnk in self.links:
            mtx[lnk.out_node.code][lnk.in_node.code] = lnk.weight
        return np.array(mtx)

    @property
    def floyd_warshall(self):
        g = self.to_matrix
        for nk in self.nodes:
            for ni in self.nodes:
                for nj in self.nodes:
                    if g[ni.code][nj.code] > g[ni.code][nk.code] + g[nk.code][nj.code]:
                        g[ni.code][nj.code] = g[ni.code][nk.code] + g[nk.code][nj.code]
        return g

    def generate(self, nodes_num, links_num, s_weight=stochastic.Stochastic()):
        """
            nodes_num - number of nodes in the net
            links_num - number of links in the net
            s_weight - stochastic variable of the links weight
        """
        # limit lower bound for the number of nodes
        if nodes_num < 2:
            nodes_num = 2
        # limit lower bound for the number of links
        if links_num < 1:
            links_num = 1
        # limit upper bound for the number of links
        if links_num > nodes_num * (nodes_num - 1):
            links_num = nodes_num * (nodes_num - 1)
        # define a set of the network nodes
        for i in range(1, nodes_num + 1):
            self.nodes.append(node.Node(i))
        # generate random set of the network links
        # ! some nodes in the network could be not linked (not achievable)
        l_num = 0  # counter for the links number
        while l_num < links_num:
            out_node = random.choice(self.nodes)
            in_node = random.choice(self.nodes)
            while out_node is in_node:
                in_node = random.choice(self.nodes)
            if not self.contains_link(out_node, in_node):
                self.add_link(out_node.code, in_node.code, s_weight.value(), True)
                l_num += 1

    def generate_demand(self, s_weight=stochastic.Stochastic(), s_int=stochastic.Stochastic()):
        t = 0
        while t < self.duration:
            t += s_int.value()
            cst = consignment.Consignment()
            cst.m_appear = t
            cst.weight = s_weight.value()
            cst.origin = random.choice(self.nodes)
            cst.destination = random.choice(self.nodes)
            while cst.origin is cst.destination:
                cst.destination = random.choice(self.nodes)
            self.demand.append(cst)

    def dijkstra(self, source):
        # 1 function Dijkstra(Graph, source):
        # 2     dist[source]:= 0                // Distance from source to source
        # 3     for each vertex v in Graph:     // Initializations
        # 4         if v != source
        # 5             dist[v]:= infinity      // Unknown distance function from source to v
        # 6             previous[v]:= undefined // Previous node in optimal path from source
        # 7         end if
        # 8         add v to Q                  // All nodes initially in Q
        # 9     end for
        # 10
        # 11    while Q is not empty:                   // The main loop
        # 12        u:= vertex in Q with min dist[u]    // Source node in first case
        # 13        remove u from Q
        # 14
        # 15        for each neighbor v of u:           // where v has not yet been removed from Q.
        # 16            alt:= dist[u] + length(u, v)
        # 17            if alt < dist[v]:               // A shorter path to v has been found
        # 18                dist[v]:= alt
        # 19                previous[v]:= u
        # 20            end if
        # 21        end for
        # 22    end while
        # 23 return dist[], previous[]
        # 24 end function
        size = max([nd.code for nd in self.nodes])
        distance = [float('inf') for _ in range(size)]
        previous = [None for _ in range(size)]
        q = self.nodes[:]
        distance[source.code - 1] = 0
        while len(q) > 0:
            u = q[0]
            min_distance = distance[u.code - 1]
            for nd in q:
                if distance[nd.code - 1] < min_distance:
                    u = nd
                    min_distance = distance[u.code - 1]
            q.remove(u)
            neighbors = [lnk.in_node for lnk in u.out_links]
            for v in neighbors:
                alt = distance[u.code - 1] + self.get_link(u, v).weight
                if alt < distance[v.code - 1]:
                    distance[v.code - 1] = alt
                    previous[v.code - 1] = u
        return previous

    def define_path(self, source, target):
        # 1 S:= empty sequence
        # 2 u:= target
        # 3 while previous[u] is defined:       // Construct the shortest path with a stack S
        # 4     insert u at the beginning of S  // Push the vertex into the stack
        # 5     u:= previous[u]                 // Traverse from target to source
        # 6 end while
        previous = self.dijkstra(source)
        u = target
        path = []
        while previous[u.code - 1] is not None:
            path.append(u)
            u = previous[u.code - 1]
        path.reverse()
        return path

    @property
    def od_matrix(self):
        od = {}
        for origin in self.nodes:
            for destination in self.nodes:
                od[(origin.code, destination.code)] = 0
        for cst in self.demand:
            od[(cst.origin.code, cst.destination.code)] += 1
        return od

    def print_od_matrix(self):
        od = self.od_matrix
        print "O/D\t",
        for nd in self.nodes:
            print "{0}\t".format(nd.code),
        print
        for origin in self.nodes:
            print "{0}\t".format(origin.code),
            for destination in self.nodes:
                print "{0}\t".format(od[(origin.code, destination.code)]),
            print

    def load_from_file(self, file_name):
        f = open(file_name, 'r')
        for data_line in f:
            data = data_line.split('\t')
            self.add_link(int(data[0]), int(data[1]), float(data[2]))
        f.close()

    def print_characteristics(self):
        """" Print out network parameters """
        print "Links list:"
        for lnk in self.links:
            print "{0} - {1}: {2}".format(lnk.out_node.code, lnk.in_node.code,\
                                          round(lnk.weight, 2))
