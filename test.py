from cbs_net.net import Net
from cbs_net.stochastic import Stochastic
import time

sender_code = 731
s_weight = Stochastic(law=1, location=0.03, scale=0.005)
# s_dist = Stcd ..stic(law=0, location=0.05, scale=0.15)

n = Net()
# n.gen_rect(size=size, s_weight=s_dist)
print("Loading the network...")
start_time = time.time()
n.load_from_file('rynek_links.txt')  # ('test_net.txt')
print("Network is loaded in", time.time() - start_time, "sec")
print("Calculating the shortest distances matrix...")
start_time = time.time()
n.sdm = n.floyd_warshall
n.sdm = 0.001 * n.sdm
print("SDM is calculated in", time.time() - start_time, "sec")

clients = []
for nd in n.nodes:
    if nd.code < 730:  # 730:
        clients.append(nd)

'''
f = open("tw_F_300_01.txt", "w")
for _ in range(300):
    start_time = time.time()
    n.gen_requests(sender=n.get_node(sender_code), nodes=clients,
                   prob=0.1, s_weight=s_weight)
    rts = n.clarke_wright(sender_code=sender_code, requests=n.demand,
                          capacity=0.15, verbose=False)
    print "Calculated in", time.time() - start_time, "sec"
    tw = 0
    for rt in rts:
        tw += rt.transport_work
        print rt
    print "Total transport work:", tw, "tkm\n"
    f.write(str(tw) + "\n")

f.close()
'''
n.gen_requests(sender=n.get_node(sender_code), nodes=clients,
               prob=0.9, s_weight=s_weight)
rts = n.genetic(sender_code=sender_code, requests=n.demand,
                capacity=0.15, verbose=True)
tw = 0
for rt in rts:
    tw += rt.transport_work
    print(rt)
print("Total transport work:", tw, "tkm")

