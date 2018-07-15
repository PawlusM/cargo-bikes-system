# import cbs_net
from cbs_net import Net
from cbs_net import Stochastic
from cbs_net import Route

size = 10
sender_code = size**2
s_weight = Stochastic(law=1, location=0.03, scale=0.005)
s_dist = Stochastic(law=0, location=0.05, scale=0.15)


n = Net()
n.gen_rect(size=size, s_weight=s_dist)
clients = []
for nd in n.nodes:
    if nd.code < size**2:
        clients.append(nd)
n.gen_requests(sender=n.get_node(sender_code), nodes=clients, prob=0.5, s_weight=s_weight)
rts = n.clarke_wright(sender_code=sender_code, requests=n.demand, capacity=0.15)
