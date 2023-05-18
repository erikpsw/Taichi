import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np

window_width = 600
window_height = 600

mode=1

def deCasteljaul(P,t):
    N=len(P)
    tmp=np.zeros((N-1,2))
    for j in range(N-1):
        tmp[j]=(1-t)*P[j]+t*P[j+1]
    for i in range(1,N-1):
        for j in range(N-i-1):
            tmp[j]=(1-t)*tmp[j]+t*tmp[j+1]
    return tmp[0]

def deBoorcox(P,i,k,t,U):#k阶B样条基函数,位置为i
    N=np.zeros()
    for j in range(N-1):
        tmp[j]=(1-t)*P[j]+t*P[j+1]
    for i in range(1,N-1):
        for j in range(N-i-1):
            tmp[j]=(1-t)*tmp[j]+t*tmp[j+1]
    return tmp[0]

gui = ti.GUI("wave", res=(window_width, window_height))

P=np.random.rand(6,2)
N=30
U=np.linspace(0,1,5)
print(U)

r0=10
cur=0
is_move=0 
if(mode==0):
    Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
if(mode==1):
    Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
while gui.running:
    mouse_x, mouse_y = gui.get_cursor_pos()
    if(gui.get_event(ti.GUI.LMB)):
        for i in range(len(P)):
            if (((mouse_x-P[i,0])**2+(mouse_y-P[i,1])**2)<=(r0/window_height)**2):
                is_move=1  
                cur=i
            if (not gui.is_pressed(ti.GUI.LMB)):
                is_move=0

    if(is_move):
        P[cur]=np.array([mouse_x,mouse_y]) 
        Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
    
    gui.lines(begin=np.array(Y[:-1]),end=np.array(Y[1:]),radius=2,color=0x51acea)
    gui.circles(P,r0,color=0xf87064)
    gui.lines(begin=np.array([P[-1],P[0]]),end=np.array([P[-2],P[1]]),radius=2)
    gui.show()
    