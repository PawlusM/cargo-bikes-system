import net
import route
import stochastic

n = net.Net()
n.duration = 50
# n.generate(10, 25, stochastic.Stochastic())
n.load_from_file("net.txt")
# for lnk in n.links:
#     lnk.weight = stochastic.Stochastic().value()
print n
n.print_sdm()
# print n.floyd_warshall
n.generate_demand()
# n.print_odm()
rts = n.clarke_wright(sender_code=0, requests=n.demand, capacity=2)
for r in rts:
    print r.weights, sum(r.weights)
