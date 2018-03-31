import net
import route
import stochastic

n = net.Net()
n.duration = 1000
n.generate(15, 500, stochastic.Stochastic())
# n.load_from_file("net.txt")
# for lnk in n.links:
#     lnk.weight = stochastic.Stochastic().value()
# n.print_characteristics()
# print n.to_matrix
# print
# print n.floyd_warshall
n.generate_demand()
# n.print_od_matrix()
n.clarke_wright(sender_code=2)
