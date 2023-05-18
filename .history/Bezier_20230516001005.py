import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

window_width = 600
window_height = 600

def deCasteljaul(P,t):
    N=len(P)
    tmp=np.zeros((N-1,2))
    for j in range(N-1):
        tmp[j]=(1-t)*P[j]+t*P[j+1]
    for i in range(1,N-1):
        for j in range(N-i-1):
            tmp[j]=(1-t)*tmp[j]+t*tmp[j+1]
    return tmp[0]

gui = ti.GUI("wave", res=(window_width, window_height))

P=np.random.rand(6,2)
N=30
Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
r0=6

while gui.running:
    mouse_x, mouse_y = gui.get_cursor_pos()
    for Pi in P:
        if (gui.get_event(ti.GUI.LMB) and ((mouse_x-Pi)**2+(mouse_y-Pi)**2)<=(r0/window_height)**2):
            is_move=1  
            Pi=np.array([mouse_x,mouse_y])          
        if (not gui.is_pressed(ti.GUI.LMB)):
            is_move=0
    
    
    gui.lines(begin=np.array(Y[:-1]),end=np.array(Y[1:]),radius=2,color=0x51acea)
    gui.circles(Y,r0)
    gui.circles(P,r0,color=0xf87064)
    gui.show()
    