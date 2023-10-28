

class Node:
    def __init__(self,theta,children=[],parent='') -> None:
        #相对与父节点的角度
        self.theta=theta
        self.children=children
        self.parent=parent
    
    def __str__(self):
        return self.theta
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        
