# import cbs_net
from cbs_net import Net
from cbs_net import Stochastic
from cbs_net import Route
import time

<<<<<<< HEAD
sender_code = 735
=======
sender_code = 734
>>>>>>> 4a40092a9b6954c5d2dbd26b5ceb91550e9f9cc1
s_weight = Stochastic(law=1, location=0.03, scale=0.005)
# s_dist = Stochastic(law=0, location=0.05, scale=0.15)


n = Net()
# n.gen_rect(size=size, s_weight=s_dist)
print "Loading the network..."
start_time = time.time()
n.load_from_file('rynek_links.txt')
print "Network is loaded in", time.time() - start_time, "sec"
print "Calculating the shortest distances matrix..."
start_time = time.time()
n.sdm = n.floyd_warshall
n.sdm = 0.001 * n.sdm
print "SDM is calculated in", time.time() - start_time, "sec"

clients = []
for nd in n.nodes:
    if nd.code < 730:
        clients.append(nd)

<<<<<<< HEAD
f = open("tw_F_300_01.txt", "w")
=======
f = open("tw_E_300_01.txt", "w")
>>>>>>> 4a40092a9b6954c5d2dbd26b5ceb91550e9f9cc1
for _ in range(300):
    start_time = time.time()
    n.gen_requests(sender=n.get_node(sender_code), nodes=clients, prob=0.1, s_weight=s_weight)
    rts = n.clarke_wright(sender_code=sender_code, requests=n.demand, capacity=0.15, verbose=False)
    print "Calculated in", time.time() - start_time, "sec"
    tw = 0
    for rt in rts:
        tw += rt.transport_work
        print rt
    print "Total transport work:", tw, "tkm\n"
    f.write(str(tw) + "\n")

f.close()
