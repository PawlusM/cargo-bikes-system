import net
import route
import stochastic
import matplotlib.pyplot as plt


size = 7
sender_code = size**2
s_weight = stochastic.Stochastic(law=1, location=0.03, scale=0.005)
s_dist = stochastic.Stochastic(law=0, location=0.05, scale=0.15)

total_TW = []
for _ in range(100):
    n = net.Net()
    n.gen_rect(size=size, s_weight=s_dist)
    clients = []
    for nd in n.nodes:
        if nd.code < sender_code:
            clients.append(nd)
    n.gen_requests(sender=n.get_node(sender_code), nodes=clients, prob=0.5, s_weight=s_weight)
    rts = n.clarke_wright(sender_code=sender_code, requests=n.demand, capacity=0.15)
    total_TW.append(sum([rt.transport_work for rt in rts]))

plt.hist(total_TW)
plt.show()
