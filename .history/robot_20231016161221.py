import taichi as ti
ti.init(arch=ti.cpu)
import numpy as np

class Node:
    def __init__(self,theta,length=0,children=[],parent='') -> None:
        #相对与父节点的角度
        self.theta=theta
        self.children=children
        self.length=length
        self.parent=parent
        self.pos
    
    def __str__(self):
        return self.theta
        
    def get_pos(self):
        cur_node=self
        arr=[]
        while(cur_node.parent!=''):
            arr.append(cur_node)

             self.pos=np.array([np.sin(self.theta)])
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        

window_width = 600
window_height = 600

gui = ti.GUI("robot", res=(window_width, window_height))
while gui.running:
    pass
    #  gui.circle(np.array([R,0]),radius=R*window_width,color=0x51acea)