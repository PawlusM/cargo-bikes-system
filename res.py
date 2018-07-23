import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
from scipy import stats

tw_diag, tw_mid = [], []
fd = open("tw_diag_300.txt", "r")
for d in fd:
    tw_diag.append(float(d))
fd.close()
fm = open("tw_mid_300.txt", "r")
for d in fm:
    tw_mid.append(float(d))
fm.close()
tw_diag, tw_mid = np.array(tw_diag), np.array(tw_mid)

print("Mean: ", tw_diag.mean(), tw_mid.mean())
print("Variance: ", tw_diag.var(), tw_mid.var())
print("Observations: ", \
      np.round(1.64**2 * tw_diag.var() / (0.05 * tw_diag.mean())**2), \
      np.round(1.64**2 * tw_mid.var() / (0.05 * tw_mid.mean())**2))
tw_diag = np.sort(tw_diag)
tw_mid = np.flipud(np.sort(tw_mid))
print()
print("Location A priority: ", (tw_diag < tw_mid).sum())

#
# plt.hist(tw_diag, normed=True)
# plt.hist(tw_mid, normed=True, color='grey')
#
# xt = plt.xticks()[0]
# xmin, xmax = min(xt), max(xt)
# lnspc = np.linspace(xmin, xmax, len(tw_diag))
#
# m_diag, s_diag = stats.norm.fit(tw_diag)
# m_mid, s_mid = stats.norm.fit(tw_mid)
# plt.plot(lnspc, stats.norm.pdf(lnspc, m_diag, s_diag), 'r--', label='lokalizacja A')
# plt.plot(lnspc, stats.norm.pdf(lnspc, m_mid, s_mid), 'g--', label='lokalizacja B')
#
# plt.legend()
# plt.xlabel('Praca przewozowa [tkm]')
# plt.ylabel('Funkcja gęstości [-]')
#
# plt.show()
