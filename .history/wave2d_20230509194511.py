import taichi as ti
import numpy as np

dt=0.1
ti.init(arch=ti.cuda)
N = 500
h=30
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(N,N))
board = ti.Vector.field(3, dtype=ti.f64, shape=(N,h))

gui = ti.GUI("wave", res=(N , N),fast_gui=True)
gui2 = ti.GUI("board", res=(N , h),fast_gui=True)
@ti.func
def get_h(A,x0,y0,x,y,lam,w,t,p0):
    d=ti.sqrt((x-x0)**2+(y-y0)**2)
    return(A*ti.cos(w*t-(6.283*d/lam)+p0))
t=0
A1=0.2
A2=0.2
@ti.kernel
def paint(t:float):
    for i, j in canvas: 
        x=i/N
        y=j/N
        canvas[i, j]-=canvas[i, j]
        canvas[i, j] += get_h(A1,0.3,0.5,x,y,0.1,0.5,t,0)+get_h(A2,0.7,0.5,x,y,0.1,0.5,t,0)
        canvas[i, j]+=A1+A2
        canvas[i, j]/=2*(A1+A2)
    
color_max=1
@ti.kernel    
def get_res():
    for i, j in board: 
        board[i, j]-=board[i, j]
        board[i, j]+=canvas[i, -1]
        if(board[i, j]>color_max):
            color_max=board[i,j]
        
while gui.running and gui2.running:
    t+=dt
    paint(t)
    get_res()
    gui.set_image(canvas)
    gui2.set_image(board)
    gui.show()
    gui2.show()