import matplotlib.pyplot as plt


tw_diag, tw_mid = [], []
fd = open("tw_diag_300.txt", "r")
for d in fd:
    tw_diag.append(float(d))
fd.close()
fm = open("tw_mid_300.txt", "r")
for d in fm:
    tw_mid.append(float(d))
fm.close()
# print tw_diag
# print len(tw_diag)
print sum(tw_diag)/len(tw_diag), sum(tw_mid)/len(tw_mid)
# plt.hist(tw_diag)
# plt.show()
