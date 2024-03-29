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


U=np.array([0,0,0,0,0.5,1,1,1,1])

k=3
P=np.random.rand(6,2)
U=np.linspace(0,1,len(P[:,1])+k+1)

# P=np.array([[0.30,0],[0.60,0.10],[0.80,0.30],[0.90,0.60],[0.90,0.90]])
# U=np.array([0,0,0,0,0.5,1,1,1,1])


def deBoorcox(P,k,u,U):#k阶B样条基函数,位置为i
    length=len(U)-1
    N=np.zeros(length)
    if(u==0):
        return P[0]
    if(u==1):
        return P[-1]
    else:
        for i in range(1,len(U)):
            if U[i]>=u:
                N[i-1]=1
                break
        for i in range(1,k+1):#迭代轮数和目前次数
            length-=1
            for j in range(length):#j为目前的i
                if(U[j+i]-U[j]==0 and U[j+i+1]-U[j+1]==0):
                    N[j]=0
                elif(U[j+i]-U[j]!=0 and U[j+i+1]-U[j+1]==0):
                    N[j]=(u-U[j])/(U[j+i]-U[j])*N[j]
                elif(U[j+i]-U[j]==0 and U[j+i+1]-U[j+1]!=0):
                    N[j]=(U[j+i+1]-u)/(U[j+i+1]-U[j+1])*N[j+1]
                elif(U[j+i]-U[j]!=0 and U[j+i+1]-U[j+1]!=0):
                    N[j]=(u-U[j])/(U[j+i]-U[j])*N[j]+(U[j+i+1]-u)/(U[j+i+1]-U[j+1])*N[j+1]     
            # print(N)
        ans=np.zeros(2)
        for i in range(len(P)):
            ans+=P[i]*N[i]
        return ans

# print(deBoorcox(P,k,1,U))
N=60
print(np.array([deBoorcox(P,2,j/N,U) for j in range(k+1,N-k-1)]).reshape(-1,2))
    


gui = ti.GUI("wave", res=(window_width, window_height))

r0=10
cur=0
is_move=0 
if(mode==0):
    Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
if(mode==1):
    Y=Y=np.array([deBoorcox(P,k,j,U) for j in np.linspace(U[k],U[-k],N)]).reshape(-1,2)
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
        if(mode==0):
            Y=np.array([deCasteljaul(P,j/N) for j in range(N+1)]).reshape(N+1,2)
        if(mode==1):
            Y=np.array([deBoorcox(P,k,j,U) for j in np.linspace(U[k],U[-k],N)]).reshape(-1,2)
    gui.lines(begin=np.array(Y[:-1]),end=np.array(Y[1:]),radius=2,color=0x51acea)
    gui.circles(P,r0,color=0xf87064)
    if(mode==0):
        gui.lines(begin=np.array([P[-1],P[0]]),end=np.array([P[-2],P[1]]),radius=2)
    gui.show()
    