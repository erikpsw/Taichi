import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
N=500

class joint:
    def __init__(self,pos,type=0,ext_F=[0,0]) -> None:
        self.pos=pos
        self.type=type#0为一般，1为支座约束，2为铰链约束
        self.F=[]
        self.ext_F=ext_F

joints=[joint([0,0],1),joint([4,0],2),joint([2,2/np.sqrt(3)]),joint([2,0],ext_F=[0,-10])]
num=len(joints)
pos=np.array([[0,0],[4,0],[2,2/np.sqrt(3)],[2,0]])
pos2=pos/5+0.1#可视化的位置
pos2[:,1]+=0.3
Adj=np.array([[0,2],[0,3],[1,2],[1,3],[2,3]])

#cur用于控制其他约束力
cur=num
A=np.zeros((2*num,2*num))
B=np.zeros(2*num)

for j in range(num):
    eqa1,eqa2=np.zeros(2*num),np.zeros(2*num)
    for i in range(len(Adj)):
        if(j in Adj[i]):
            index=Adj[i][1] if Adj[i][0]==j else Adj[i][0]
            tmp=pos[index]-pos[j]
            dir=tmp/(tmp.dot(tmp)**0.5)
            eqa1[i]=dir[0]#x方向
            eqa2[i]=dir[1]#y方向
    if(joints[j].type==1):
        eqa2[cur+1]=1
        cur+=1
    if(joints[j].type==2):
        eqa1[cur+1]=1
        eqa2[cur+2]=1
        cur+=2
    A[2*j,:]=eqa1
    A[2*j+1,:]=eqa2
    obj=joints[j]
    if(obj!=[0,0]):
        B[2*j]=-obj.ext_F[0]
        B[2*j+1]=-obj.ext_F[1]
        
ans=linalg.solve(A,B)

x = pos[Adj[:,0]]
y = pos[Adj[:,1]]
print(y)
for i in range(num):
    plt.scatter(pos[i][0],pos[i][1], color='black', s=5)
for i in range(len(x)):
    plt.plot([x[i][0],y[i][0]],[x[i][1],y[i][1]], label='sin')
    plt.annotate(str(ans[i]),[(x[i][0]+y[i][0])/2,(x[i][1]+y[i][1])/2])
plt.xlim(-1,5)
plt.ylim(-1,3)
plt.show()