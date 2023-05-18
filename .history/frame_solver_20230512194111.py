import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
N=500

def rgba_to_hex(rgba):
    r = int(rgba[0] * 255)
    g = int(rgba[1] * 255)
    b = int(rgba[2] * 255)
    a = int(rgba[3] * 255)
    hex_code = "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)
    return hex_code

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

data = ans[:num+1]

# 选择一个colormap
cmap = plt.cm.get_cmap('viridis')

# 对数据进行归一化，将值映射到[0, 1]的区间
normalized_data = (data - data.min()) / (data.max() - data.min())

# 将归一化后的数据传入colormap中，得到对应的颜色数组
colors = cmap(normalized_data)



for i in range(len(x)):
    plt.plot([x[i][0],y[i][0]],[x[i][1],y[i][1]],color=rgba_to_hex(colors[i]))
    plt.annotate(str(round(ans[i],1)),[(x[i][0]+y[i][0])/2,(x[i][1]+y[i][1])/2])
plt.xlim(-0.5,4.5)
plt.ylim(-0.5,2.3)
plt.colorbar(cmap)
plt.show()