class Node:
    def __init__(self,theta,children=[],parent='') -> None:
        self.theta=theta
        self.children=children
        self.parent=parent
    
    def __str__(self):
        return
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        
        