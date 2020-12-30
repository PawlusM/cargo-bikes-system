from cbs_net import Stochastic

# 731 obiekt
# R 	Restauracja - 12 zam./mies. - 50 kg
# H	    Hotel       - 10 zam./mies. - 150 kg
# B	    Bar         - 8 zam./mies.  - 100 kg
# K	    Kawiarnia   - 16 zam./mies. - 50 kg
# S	    Sklep       - 10 zam./mies. - 400 kg
# Ks	Ksiegarnia  - 2 zam./mies.  - 500 kg

clients = []
freqs = {'R': 12.0, 'H': 10.0, 'B': 8.0, 'K': 16.0, 'S': 10.0, 'Ks': 2.0}
weights = {'R': 50.0, 'H': 150.0, 'B': 100.0, 'K': 50.0, 'S': 400.0, 'Ks': 500.0}

f = open('rynek.txt', 'r')
for data_line in f:
    data = data_line.split('\t')
    clients.append({'name': str(data[1]), 'type': str(data[2])})
f.close()
# print clients


duration = 24 * 30.0 # a month
requests = []
for client in clients:
    itvl = Stochastic(law=2, scale=duration/freqs[client['type']])
    weight = Stochastic(law=1, \
                        location=weights[client['type']], \
                        scale=0.25*weights[client['type']])
    t = itvl.value()
    w = weight.value()
    while t < duration:
        #print t, w
        requests.append((t, w, client['type'], client['name']))
        t += itvl.value()
        w = weight.value()

requests.sort(key = lambda r: r[0])

f = open("demand.txt", "w")
for r in requests:
    f.write(str(round(r[0], 2)) + "\t" + str(round(r[1], 2)) + "\t" +
            r[2] + "\t" + r[3] + "\n")
    print r
f.close()