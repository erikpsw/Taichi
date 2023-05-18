import taichi as ti

dt=0.1
ti.init(arch=ti.cuda)
N = 500
h=0.5
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(N,N))

gui = ti.GUI("wave", res=(N , N),fast_gui=True)

t=0
dt=0.05
A1=0.2
A2=0.2
lamb=1
d=0.1
@ti.kernel
def paint(t:float):
    for i, j in canvas: 
        x=i/N
        y=j/N
        delta=2*
        d=ti.sqrt((x-0.5)**2+(y-0.5)**2)
        theta=ti.atan2(h,d)
        canvas[i, j]-=canvas[i, j]
        canvas[i, j]+=ti.cos(theta)



        
while gui.running:
    t+=dt
    paint(t)
    gui.set_image(canvas)
    gui.show()