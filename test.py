import net
import route
import stochastic

n = net.Net()
n.duration = 100
n.generate(5, 10, stochastic.Stochastic())
# n.print_characteristics()
# print n.to_matrix
# print
print n.floyd_warshall
r = route.Route(n)
r.nodes = [n.get_node(1)] + n.define_path(n.get_node(1), n.get_node(5))
print [nd.code for nd in r.nodes]
print r.distance
n.generate_demand()
n.print_od_matrix()
