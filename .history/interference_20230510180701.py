import taichi as ti

dt=0.1
ti.init(arch=ti.cuda)
N = 500
h=0.5
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
        d=ti.sqrt((x-0.5)**2+(y-0.5)**2)
        theta=ti.atan2(h/d)
        canvas[i, j]-=canvas[i, j]
        canvas[i, j]+=ti.cos(theta)



        
while gui.running and gui2.running:
    t+=dt
    paint(t)
    gui.set_image(canvas)
    gui.show()