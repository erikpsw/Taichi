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

N=10
Y=[]

for j in range(N+1):
    Y.append(deCasteljaul(P,j/N))
Y=np.array(Y).reshape(N+1,2)
print(Y)

while gui.running:
    gui.circles(Y,3)
    gui.lines(begin=np.array(Y[:-1]),end=np.array(Y[1:]),radius=2,color=0xf87064)
    gui.show()
    