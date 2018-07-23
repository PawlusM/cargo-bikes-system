import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
from scipy import stats

files = ["tw_A_300_01.txt", "tw_B_300_01.txt", "tw_C_300_01.txt",
         "tw_D_300_01.txt"]
tws = [[] for _ in files]

for i in range(len(files)):
    f = open(files[i], "r")
    for d in f:
        tws[i].append(float(d))
    f.close()

tws = np.array(tws)
# print tws

print("Mean\tVar.\tObs.num.")
for i in range(len(tws)):
    print("{}\t{}\t{}".format(tws[i].mean(),
                              tws[i].var(),
                              np.round(1.64**2 * tws[i].var() / (0.05 * tws[i].mean())**2)))

# tw_diag = np.sort(tw_diag)
# tw_mid = np.flipud(np.sort(tw_mid))
# print()
# print("Location A priority: ", (tw_diag < tw_mid).sum())

#
for i in range(len(tws)):
    plt.hist(tws[i], normed=True)

xt = plt.xticks()[0]
xmin, xmax = min(xt), max(xt)
lnspc = np.linspace(xmin, xmax, len(tws[0]))

m, s = [0 for _ in files], [0 for _ in files]

for i in range(len(tws)):
    m[i], s[i] = stats.norm.fit(tws[i])
    plt.plot(lnspc, stats.norm.pdf(lnspc, m[i], s[i]), label='lokalizacja ' + str(i + 1))

plt.legend()
plt.xlabel('Transport work [tkm]')
plt.ylabel('Density function [-]')

plt.show()
