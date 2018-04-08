import matplotlib.pyplot as plt


tw_diag, tw_mid = [], []
fd = open("tw_diag.txt", "r")
for d in fd:
    tw_diag.append(float(d))
print tw_diag
print len(tw_diag)
print sum(tw_diag)/len(tw_diag)
plt.hist(tw_diag)
plt.show()
