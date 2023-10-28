class Node:
    def __init__(self,theta,children=[],parent='') -> None:
        self.theta=theta
        self.children=children
        self.parent=parent
        
class Robot:
    def __init__(self,root) -> None:
        self.root=root
        