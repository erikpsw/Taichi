# import taichi as ti
import numpy as np

# ti.init(arch=ti.cuda)
N=500
# gui = ti.GUI("wave", res=(N , N))
class joint:
    def __init__(self,pos,type=0,ext_F=0) -> None:
        self.pos=pos
        self.type=type#0为一般，1为支座约束，2为铰链约束
        self.F=[]
        self.ext_F=ext_F

joints=[joint([0,0],1),joint([4,0],2),joint([2,2/np.sqrt(3)]),joint([2,0],ext_F=-10)]
num=len(joints)
pos=np.array([[0,0],[4,0],[2,2/np.sqrt(3)],[2,0]])
pos2=pos/5+0.1#可视化的位置
pos2[:,1]+=0.3
Adj=np.array([[0,2],[0,3],[1,2],[1,3],[2,3]])

for j in range(num):
    eqa=np.zeros(2*num)
    for i in range(len(Adj)):
        if(j in Adj[i]):
            index=Adj[i][1] if Adj[i][0]==j else Adj[i][0]
            dir=(pos[index]-pos[j])/(pos[index]-pos[j]).dot()**0.5
            print()
    # if(joints[j].type==1):
        


# while gui.running:
#     gui.lines(pos2[Adj[:,0]],pos2[Adj[:,1]],radius=3,color=0x51acea)
#     gui.show()