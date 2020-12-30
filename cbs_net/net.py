import random
import numpy as np
import time

from cbs_net.stochastic import Stochastic
from cbs_net.link import Link
from cbs_net.node import Node
from cbs_net.consignment import Consignment
from cbs_net.route import Route

# from satsp import solver as slv  # TSP solver by simulated annealing
from cbs_ga.ga_tsp import GA


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
        # servicing facilities
        self.fleet = []
        self.load_points = []
        # shortest distances od_matrix
        self.sdm = np.array([[]])

    def __str__(self):
        ans = "The network configuration:\n"
        for lnk in self.links:
            ans += "{0}\t-\t{1}:\t{2}\n".format(lnk.out_node.code,\
                                                lnk.in_node.code,\
                                                round(lnk.weight, 2))
        return ans

    def contains_node(self, code):
        """" Determines if the network contains a node with the specified code """
        for n in self.nodes:
            if n.code == code:
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
        for lnk in self.links:
            if lnk.out_node is out_node and lnk.in_node is in_node:
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
                    new_link = Link(out_node, in_node, weight)
                    out_node.out_links.append(new_link)
                    in_node.in_links.append(new_link)
                    self.links.append(new_link)
            else:
                # the net contains the specified out-node, but there is no in-node with the specified code
                in_node = Node(in_code)
                new_link = Link(out_node, in_node, weight)
                out_node.out_links.append(new_link)
                in_node.in_links.append(new_link)
                self.nodes.append(in_node)
                self.links.append(new_link)
        else:
            # the net does not contain the specified out-node
            out_node = Node(out_code)
            if self.contains_node(in_code):
                # in-node is already in the net
                in_node = self.get_node(in_code)
            else:
                # there are no in-node and out-node with the specified codes
                in_node = Node(in_code)
                self.nodes.append(in_node)
            # create new link
            new_link = Link(out_node, in_node, weight)
            out_node.out_links.append(new_link)
            in_node.in_links.append(new_link)
            self.nodes.append(out_node)
            self.links.append(new_link)
        # add the reverse link
        if not directed:
            self.add_link(in_code, out_code, weight, True)

    @property
    def to_matrix(self):
        self.nodes.sort(key=lambda nd: nd.code)  # sort the nodes!
        mtx = np.array([[np.inf for _ in self.nodes] for __ in self.nodes])
        for nd in self.nodes:
            mtx[nd.code][nd.code] = 0
        for lnk in self.links:
            mtx[lnk.out_node.code][lnk.in_node.code] = lnk.weight
        return mtx

    @property
    def floyd_warshall(self):
        g = self.to_matrix
        for nk in self.nodes:
            for ni in self.nodes:
                for nj in self.nodes:
                    if g[ni.code][nj.code] > g[ni.code][nk.code] + g[nk.code][nj.code]:
                        g[ni.code][nj.code] = g[ni.code][nk.code] + g[nk.code][nj.code]
        return g

    def gen_rect(self, size=2, s_weight=Stochastic()):
        # reset the current configuration
        self.nodes, self.links = [], []
        # generate nodes
        for i in range(size * size + 4 * (size - 1)):
            # 1..size**2 are inner nodes,
            # (size**2 + 1)..(size**2 + 4 * (size - 1)) are edge nodes
            self.nodes.append(Node(i))
        # generate links between inner nodes
        for i in range(size):
            for j in range(1, size):
                self.add_link(size * i + j - 1, size * i + j, s_weight.value())
                self.add_link(size * (j - 1) + i, size * j + i, s_weight.value())
        # generate links for edge nodes
        for i in range(size):
            # top edge
            self.add_link(i, size * size + i, s_weight.value())
            # bottom edge
            self.add_link(size * (size - 1) + i, size * (size + 1) + i, s_weight.value())
        for i in range(size - 2):
            # left edge
            self.add_link((i + 1) * size, size * (size + 2) + i, s_weight.value())
            # right edge
            self.add_link((i + 2) * size - 1, size * (size + 3) - 2 + i, s_weight.value())

    def generate(self, nodes_num, links_num, s_weight=Stochastic()):
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
        # reset the current configuration
        self.nodes, self.links = [], []
        # define a set of the network nodes
        for i in range(nodes_num):
            self.nodes.append(Node(i))
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

    def gen_requests(self, sender=None, nodes=[], prob=1, s_weight=Stochastic(), verbose=True):
        self.demand = []
        for nd in nodes:
            if random.random() < prob:
                cst = Consignment()
                cst.origin, cst.destination = sender, nd
                cst.weight = s_weight.value()
                self.demand.append(cst)
        if verbose:
            print("Demand generation completed: {} requests generated.".format(len(self.demand)))

    def gen_req_flow(self, s_weight=Stochastic(), s_int=Stochastic(), verbose=True):
        t = 0
        self.demand = []
        while t < self.duration:
            t += s_int.value()
            cst = Consignment()
            cst.m_appear = t
            cst.weight = s_weight.value()
            cst.origin = random.choice(self.nodes)
            cst.destination = random.choice(self.nodes)
            while cst.origin is cst.destination:
                cst.destination = random.choice(self.nodes)
            self.demand.append(cst)
        if verbose:
            print("Demand generation completed: {} requests generated.".format(len(self.demand)))

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
        size = len(self.nodes)
        distance = [np.inf for _ in range(size)]
        previous = [None for _ in range(size)]
        q = self.nodes[:]
        distance[source.code] = 0
        while len(q) > 0:
            u = q[0]
            min_distance = distance[u.code]
            for nd in q:
                if distance[nd.code] < min_distance:
                    u = nd
                    min_distance = distance[u.code]
            q.remove(u)
            neighbors = [lnk.in_node for lnk in u.out_links]
            for v in neighbors:
                alt = distance[u.code] + self.get_link(u, v).weight
                if alt < distance[v.code]:
                    distance[v.code] = alt
                    previous[v.code] = u
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
        while previous[u.code] is not None:
            path.append(u)
            u = previous[u.code]
        path.reverse()
        return path

    def clarke_wright(self, sender_code=0, requests=[], capacity=10, verbose=True):
        routes = []  # the calculated routes
        n = len(self.nodes)  # number of nodes in the net

        # choose only consignments with sender as origin
        sender = self.get_node(sender_code)  # sernder's node
        from_sender = []
        for cst in requests:
            if cst.origin is sender:
                from_sender.append(cst)
        # combine multiple consignments for the same destination
        if verbose:
            print("Combining multiple consignments...")
        combined_weights = [0 for _ in range(n)]
        for cst in from_sender:
            combined_weights[cst.destination.code] += cst.weight
        combined = []  # set of consignments combined by consignees
        consignee_codes = []
        for i in range(n):
            if combined_weights[i] > 0:
                combined.append(Consignment(combined_weights[i],
                                            sender, self.get_node(i)))
                consignee_codes.append(i)
        if verbose:
            print(sender_code, consignee_codes)
        # number of consignees
        m = len(consignee_codes)

        # get SDM for the routing problem
        d = np.array([[np.inf for _ in range(m + 1)]
                      for __ in range(m + 1)])
        d[0][0] = self.sdm[sender_code][sender_code]
        for i in range(1, m + 1):
            d[0][i] = self.sdm[sender_code][consignee_codes[i - 1]]
            d[i][0] = self.sdm[consignee_codes[i - 1]][sender_code]
            for j in range(1, m + 1):
                d[i][j] = self.sdm[consignee_codes[i - 1]][consignee_codes[j - 1]]
        if verbose:
            print("\nSDM for the routing problem:")
            print(d)

        if verbose:
            print("\nClarke-Wright algorithm started...")

        def route_of(nd):
            for route in routes:
                if nd in route.nodes:
                    return route
            return None

        def are_in_same_route(nd1, nd2):
            for route in routes:
                if nd1 in route.nodes and nd2 in route.nodes:
                    return True
            return False

        def is_in_head(nd, route):
            if route is None or nd not in route.nodes:
                return False
            return route.nodes.index(nd) == 1

        def is_in_tail(nd, route):
            if route is None or nd not in route.nodes:
                return False
            return route.nodes.index(nd) == route.size

        def is_head_or_tail(nd):
            route = route_of(nd)
            return route is not None and (is_in_head(nd, route) or is_in_tail(nd, route))

        # forming the set of simple routes (pendular with empty returns)
        for cst in combined:
            route = Route(self, [cst])
            routes.append(route)
        # calculating the wins matrix
        if verbose:
            print("\nCalculating the wins matrix...")
        start_time = time.time()
        s = np.array([[0.0 for _ in range(m)]
                      for __ in range(m)])  # wins matrix
        for i in range(m):
            for j in range(m):
                if j < i:
                    s[i][j] = d[0][i] + d[0][j] - d[i][j]
                else:
                    s[i][j] = -np.inf
        if verbose:
            print("\nWins matrix for the routing problem (calculated in {} sec):".format(time.time() - start_time))
            print(s)
            print("\nForming the routes...")
        start_time = time.time()
        # start the routes merging
        while True:
            max_s = -np.inf
            i_max, j_max = 0, 0
            for i in range(m):
                for j in range(m):
                    if s[i][j] > max_s:
                        max_s = s[i][j]
                        i_max, j_max = i, j
            s[i_max][j_max] = -np.inf
            r1 = route_of(self.nodes[consignee_codes[i_max]])
            r2 = route_of(self.nodes[consignee_codes[j_max]])
            # conditions to be fulfilled for segments merging
            if not are_in_same_route(self.nodes[consignee_codes[i_max]],
                                     self.nodes[consignee_codes[j_max]]) and \
                    is_head_or_tail(self.nodes[consignee_codes[i_max]]) and \
                    is_head_or_tail(self.nodes[consignee_codes[j_max]]) and \
                    r1.weight + r2.weight <= capacity:
                # checking the side before merging
                if r1.size > 1:
                    if is_in_tail(self.nodes[consignee_codes[i_max]], r1):
                        if r2.size > 1 and is_in_tail(self.nodes[consignee_codes[j_max]], r2):
                            r2.nodes.reverse()
                        r1.merge(r2)
                        routes.remove(r2)
                    else:
                        if r2.size > 1 and is_in_head(self.nodes[consignee_codes[j_max]], r2):
                            r2.nodes.reverse()
                        r2.merge(r1)
                        routes.remove(r1)
                else:
                    if is_in_tail(self.nodes[consignee_codes[j_max]], r2):
                        r2.merge(r1)
                        routes.remove(r1)
                    else:
                        r1.merge(r2)
                        routes.remove(r2)
            # checking if the optimization procedure is complete
            if max_s == -np.inf:
                break
        # printing the routes to console
        if verbose:
            print("{} routes were formed in {} sec.".format(len(routes), time.time() - start_time))
            for rt in routes:
                print(rt)
        # return the list of routes
        return routes

    @staticmethod
    def get_batches(self, consignments, batch_size):
        indices = [idx for idx in range(len(consignments))]
        batches = []
        random.shuffle(indices)
        while len(indices) > 0:
            batch, total_weight = [], 0
            while len(indices) > 0 and total_weight < batch_size:
                idx = indices[0]
                batch.append(consignments[idx])
                total_weight += consignments[idx].weight
                indices.remove(idx)
            # print([(r.origin.code, r.destination.code) for r in batch])
            batches.append(batch)
        return batches

    def annealing(self, sender_code=0, requests=[], capacity=10, verbose=True):
        pass
        # routes = []  # the calculated routes
        # n = len(self.nodes)  # number of nodes in the net
        #
        # # choose only consignments with sender as origin
        # sender = self.get_node(sender_code)  # sender's node
        # from_sender = []
        # for cst in requests:
        #     if cst.origin is sender:
        #         from_sender.append(cst)
        # # combine multiple consignments for the same destination
        # if verbose:
        #     print("Combining multiple consignments...")
        # combined_weights = [0 for _ in range(n)]
        # for cst in from_sender:
        #     combined_weights[cst.destination.code] += cst.weight
        # combined = []  # set of consignments combined by consignees
        # consignee_codes = []
        # for i in range(n):  # consignee codes start from 0
        #     if combined_weights[i] > 0:
        #         combined.append(Consignment(combined_weights[i],
        #                                     sender, self.get_node(i)))
        #         consignee_codes.append(i)
        # if verbose:
        #     print(sender_code, consignee_codes)
        # # define batches
        # batches = self.get_batches(self, consignments=combined, batch_size=capacity)
        # for batch in batches:
        #     nodes = [sender]
        #     nodes.extend([cst.destination for cst in batch])
        #     if len(batch) > 1:
        #         slv.Solve(dist_matrix=[[self.sdm[nd1.code][nd2.code]
        #                                 for nd2 in nodes]
        #                                for nd1 in nodes],
        #                   screen_output=verbose)
        #         routes.append(Route(net=self,
        #                             csts=[batch[idx - 2]
        #                                   for idx in slv.GetBestTour()[1:]]))
        #     else:
        #         routes.append(Route(net=self, csts=batch))
        #
        # # return the list of routes
        # return routes

    def genetic(self, sender_code=0, requests=[], capacity=10, verbose=True):
        routes = []  # the calculated routes
        n = len(self.nodes)  # number of nodes in the net

        # choose only consignments with sender as origin
        sender = self.get_node(sender_code)  # sender's node
        from_sender = []
        for cst in requests:
            if cst.origin is sender:
                from_sender.append(cst)
        # combine multiple consignments for the same destination
        if verbose:
            print("Combining multiple consignments...")
        combined_weights = [0 for _ in range(n)]
        for cst in from_sender:
            combined_weights[cst.destination.code] += cst.weight
        combined = []  # set of consignments combined by consignees
        consignee_codes = []
        for i in range(n):  # consignee codes start from 0
            if combined_weights[i] > 0:
                combined.append(Consignment(combined_weights[i],
                                            sender, self.get_node(i)))
                consignee_codes.append(i)
        if verbose:
            print(sender_code, consignee_codes)
        # define batches
        batches = self.get_batches(self, consignments=combined, batch_size=capacity)
        for batch in batches:
            nodes = [sender]
            nodes.extend([cst.destination for cst in batch])
            winner = GA(mtx=[[self.sdm[nd1.code][nd2.code]
                              for nd2 in nodes]
                             for nd1 in nodes]).evolve(verbose=verbose)
            routes.append(Route(net=self,
                                csts=[batch[idx - 1]
                                      for idx in winner.order]))

        # return the list of routes
        return routes

    @property
    def od_matrix(self):
        od = {}
        for origin in self.nodes:
            for destination in self.nodes:
                od[(origin.code, destination.code)] = 0
        for cst in self.demand:
            od[(cst.origin.code, cst.destination.code)] += 1
        return od

    def print_odm(self):
        pass
        # od = self.od_matrix
        # print("O/D", end='\t')
        # for nd in self.nodes:
        #     print(nd.code, end='\t')
        # print()
        # for origin in self.nodes:
        #     print(origin.code, end='\t')
        #     for destination in self.nodes:
        #         print(od[(origin.code, destination.code)], end='\t')
        #     print()

    def print_sdm(self):
        pass
        # print("SDM", end='\t')
        # for nd in self.nodes:
        #     print(nd.code, end='\t')
        # print()
        # for i in range(len(self.nodes)):
        #     print(self.nodes[i].code, end='\t')
        #     for j in range(len(self.nodes)):
        #         print(round(self.sdm[i][j], 3), end='\t')
        #     print()

    def load_from_file(self, file_name, dlm='\t'):
        f = open(file_name, 'r')
        for data_line in f:
            data = data_line.split(dlm)
            # print int(data[0]), int(data[1]), float(data[2])
            self.add_link(int(data[0]), int(data[1]), float(data[2]))
        f.close()
