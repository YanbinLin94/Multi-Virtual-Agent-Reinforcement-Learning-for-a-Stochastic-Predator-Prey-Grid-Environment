import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

csv_dataM1_eps5 = pd.read_csv('Q_learning_M3-P4321-eps0.01-50runs5000episode.csv',skiprows= lambda x: x>0 and (x-1)%10 !=0)
csv_dataM1_eps10 = pd.read_csv('Q_learning_M3-P4321-eps0.1-50runs5000episode.csv',skiprows= lambda x: x>0 and (x-1)%10 !=0)
csv_dataM1_eps30 = pd.read_csv('Q_learning_M3-P4321-eps0.3-50runs5000episode.csv',skiprows= lambda x: x>0 and (x-1)%10 !=0)
csv_dataM1_eps50 = pd.read_csv('Q_learning_M3-P4321-eps0.6-50runs5000episode.csv',skiprows= lambda x: x>0 and (x-1)%10 !=0)
csv_dataM1_eps80 = pd.read_csv('Q_learning_M3-P4321-eps0.8-50runs5000episode.csv',skiprows= lambda x: x>0 and (x-1)%10 !=0)

Prob1 = csv_dataM1_eps5.iloc[:,1]
Prob2 = csv_dataM1_eps10.iloc[:,1]
Prob3 = csv_dataM1_eps30.iloc[:,1]
Prob4 = csv_dataM1_eps50.iloc[:,1]
Prob5 = csv_dataM1_eps80.iloc[:,1]

figsize = 6,6
figure, ax =plt.subplots(figsize=figsize)
plt.xlim((0,5000))
plt.ylim(0,0.8)
x = [y*100 for y in range(51)]

A, = plt.plot(x,Prob1,marker='o',ms=5,mew=1, label ='epsilon=0.01')
B, = plt.plot(x,Prob2,marker='*',ms=5,mew=1, label='epsilon=0.1')
C, = plt.plot(x,Prob3,marker='+',ms=5,mew=1, label='epsilon=0.3')
D, = plt.plot(x,Prob4,marker='.',ms=5,mew=1, label ='epsilon=0.6')
E, = plt.plot(x,Prob5,marker='s',ms=5,mew=1, label ='epsilon=0.8')

plt.tick_params(labelsize=16)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Time New Roman') for label in labels]
plt.ylabel('Win probability',fontsize=19)
plt.xlabel('Episodes',fontsize=20)
font1 ={'family':'Times New Roman',
        'weight':'normal',
        'size':20,
        }
legend = plt.legend(handles=[A,B,C,D,E],prop=font1)
plt.savefig("fig1-5000.png", dpi=300)
plt.show()

