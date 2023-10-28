import taichi as ti
ti.init(arch=ti.cpu)
import numpy as np

class Node:
    def __init__(self,id,theta,length=0,children=[],parent='') -> None:
        #相对与父节点的角度
        self.theta=np.radians(theta)
        self.children=children
        self.length=length
        self.parent=parent
        self.pos=''
        self.id=id
    
    def __str__(self):
        return f'id={self.id}'
        
    def add_parents(self):
        for child in self.children:
            child.parent=self
            child.add_parents()
            
    def get_pos(self):
        cur_node=self
        arr=[]
        while(cur_node.parent!=''):
            arr.append(cur_node)
            cur_node=cur_node.parent
        print(arr)
        # self.pos=np.array([np.sin(self.theta)])
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        
window_width = 600
window_height = 600
n2=Node(2,90,3)
root=Node(0,0,children=[Node(1,90,3,children=[n2])])
root.add_parents()
n2.get_pos()
print(root.children[0])
# gui = ti.GUI("robot", res=(window_width, window_height))
# while gui.running:
#     pass
    #  gui.circle(np.array([R,0]),radius=R*window_width,color=0x51acea)