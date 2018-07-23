import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
from scipy import stats

files = {'A': 'tw_A_300_01.txt', 'B': 'tw_B_300_01.txt', 'C': 'tw_C_300_01.txt',
         'D': 'tw_D_300_01.txt'}
tws = [[] for _ in files]

# print files
# print files.keys()

for i in range(len(files)):
    f = open(files[files.keys()[i]], "r")
    for d in f:
        tws[i].append(float(d))
    f.close()

tws = np.array(tws)
# print tws

print("{:>10}\t{:>10}\t{:>10}".format("Mean", "Variance", "Obs."))
for i in range(len(tws)):
    print("{:10.3f}\t{:10.4f}\t{:10d}".format(tws[i].mean(),
                              tws[i].var(),
                              int(np.round(1.64**2 * tws[i].var() / (0.05 * tws[i].mean())**2))))

# tw_diag = np.sort(tw_diag)
# tw_mid = np.flipud(np.sort(tw_mid))
# print()
# print("Location A priority: ", (tw_diag < tw_mid).sum())

#
for i in range(len(tws)):
    plt.hist(tws[i], density=True)

xt = plt.xticks()[0]
xmin, xmax = min(xt), max(xt)
lnspc = np.linspace(xmin, xmax, len(tws[0]))

m, s = [0 for _ in files], [0 for _ in files]

for i in range(len(tws)):
    m[i], s[i] = stats.norm.fit(tws[i])
    plt.plot(lnspc, stats.norm.pdf(lnspc, m[i], s[i]), label='lokalizacja ' + files.keys()[i])

plt.legend()
plt.xlabel('Transport work [tkm]')
plt.ylabel('Density function [-]')

plt.show()
