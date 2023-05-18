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

while gui.running:
    gui.lines(begin=np.array(Y[:-1]),end=np.array(Y[1:]),radius=2,color=0x51acea)
    gui.circles(Y,6)
    gui.circles(P,6,color=0xf87064)
    gui.show()
    