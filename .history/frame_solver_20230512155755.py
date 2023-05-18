# import taichi as ti
import numpy as np

# ti.init(arch=ti.cuda)
N=500
# gui = ti.GUI("wave", res=(N , N))
class joint:
    def __init__(self,pos,type=0) -> None:
        self.pos=pos
        self.type=type#0为一般，1为支座约束，2为铰链约束
        self.F=[]

joints=[joint([0,0]),joint([4,0]),joint([2,2/np.sqrt(3)]),joint([2,0])]
pos=np.array([[0,0],[4,0],[2,2/np.sqrt(3)],[2,0]])
pos2=pos/5+0.1#可视化的位置
pos2[:,1]+=0.3
Adj=np.array([[0,2],[0,3],[1,2],[1,3],[2,3]])


# while gui.running:
#     gui.lines(pos2[Adj[:,0]],pos2[Adj[:,1]],radius=3,color=0x51acea)
#     gui.show()