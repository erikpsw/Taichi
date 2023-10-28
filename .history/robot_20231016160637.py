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
    
    def __str__(self):
        return self.theta
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        

window_width = 600
window_height = 600

gui = ti.GUI("robot", res=(window_width, window_height))
while gui.running: