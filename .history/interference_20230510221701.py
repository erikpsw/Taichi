import taichi as ti

dt=0.1
ti.init(arch=ti.cuda)
N = 500
h=0.1
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(N,N))

gui = ti.GUI("wave", res=(N , N),fast_gui=True)

t=0
dt=0.05
A1=0.2
A2=0.2
lamb=0.4
d=0.1
n1=1
n2=1.38
@ti.kernel
def paint(t:float):
    for i, j in canvas: 
        x=i/N
        y=j/N
        d=ti.sqrt((x-0.5)**2+(y-0.5)**2)
        theta=ti.atan2(h,d)
        delta=2*d*ti.sqrt(n2**2-(n1**2)*(ti.cos(theta)**2))+(lamb/2)
        dphi=delta*3.1415*2/lamb
        canvas[i, j]-=canvas[i, j]
        # canvas[i, j]+=0.25*(ti.cos(t)+ti.cos(t+dphi))+0.5
        canvas[i, j]+=ti.cos(dphi)**2



        
while gui.running:
    t+=dt
    paint(t)
    gui.set_image(canvas)
    gui.show()