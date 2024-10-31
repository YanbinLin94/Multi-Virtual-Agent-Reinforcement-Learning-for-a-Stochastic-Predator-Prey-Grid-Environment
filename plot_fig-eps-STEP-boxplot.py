import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Step_M3-P4321-eps5-10-30-50-80.csv',skiprows=lambda x: x>0 and (x-1)%100 !=0)
plt.rcParams["figure.figsize"] = [6, 5.5]
plt.rcParams["figure.autolayout"] = True

ax2 = df.plot.box()
plt.tick_params(labelsize=20)
labels = ax2.get_xticklabels() + ax2.get_yticklabels()
[label.set_fontname('Time New Roman') for label in labels]
plt.ylabel('Average step per episode',fontsize=22)
plt.xlabel('Epsilons',fontsize=22)
plt.savefig("fig4.png", dpi=300)
plt.show()



