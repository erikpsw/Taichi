import taichi as ti
import numpy as np

dt=0.01
ti.init(arch=ti.cuda)
N = 300
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(N,N))

gui = ti.GUI("Mandelbrot Set", res=(N , N),fast_gui=True)#使gpu用快速渲染

def get_h(A,x0,y0,x,y,lam,w,t,p0):
    d=ti.sqrt((x-x0)**2+(y-y0)**2)
    return(A*ti.cos(w*t-(6.283*d/lam)+p0))
t=5
A1=0.2
@ti.kernel
def paint():
    for i, j in canvas: 
        x=i/N
        y=j/N
        canvas[i, j] += get_h(0.2,0.3,0.3,x,y,0.2,0.5,t,0)+get_h(0.15,0.7,0.7,x,y,0.2,0.5,t,0)

while gui.running:
    paint()
    gui.set_image(canvas)
    gui.show()