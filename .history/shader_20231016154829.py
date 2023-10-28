import taichi as ti
import palettable
import numpy as np

@ti.func
def value2color(d):
    c1 = (1, 0, 0) 
    c2 = (0, 1, 0)  
    c3 = (0, 0, 1)  

    r = ti.abs(ti.sin(c1[0] + (c2[0] - c1[0]) * d+t))
    g = ti.abs(ti.sin(c2[1]  * (0.5+d) +3*t))
    b = ti.abs(ti.sin(c3[2] - (c3[2] - c2[2]) * (1-d) +2*t))
    
    return (r,g,b)
@ti.func
def step(depth,frac_width,ir,jr,t):
    ans=0.0
    for k in range(depth):
        frac_width=int(frac_width/frac)
        ir=ir%frac_width
        jr=jr%frac_width
        xr=ir/frac_width
        yr=jr/frac_width
        dr=ti.abs(ti.sin(6*ti.sqrt((xr-0.5)**2+(yr-0.5)**2)+3*t)*ti.exp(-ti.cos((xr-0.5)**2+(yr-0.5)**2)))
        ans=ans+0.02/dr
    return ans

frac=2
dt=0.1
# ti.init(arch=ti.cuda)
ti.init(arch=ti.cpu)
N = 800
frac_width=int(N/frac)
canvas_width=N
canvas_height=N
h=30
depth=2
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(canvas_width,canvas_height))

gui = ti.GUI("shader", res=(N , N),fast_gui=True)

@ti.kernel
def paint(t:ti.f64):
    for i, j in canvas: 
        xr=i/canvas_width
        yr=j/canvas_height
        dr=ti.abs(ti.sin(6*ti.sqrt((xr-0.5)**2+(yr-0.5)**2)+3*t))
        cr=0.04/dr
        ir=i%frac_width
        jr=j%frac_width
        cr+=step(3,frac_width,ir,jr,t)
        
        x=i/canvas_width
        y=j/canvas_height
        d=ti.sqrt(2)*ti.sqrt((x-0.5)**2+(y-0.5)**2+3*t)
        canvas[i, j]= value2color(d)*cr
    

t=0
while gui.running:
    t+=0.01
    m=t-ti.floor(t)
    ans=palettable.cartocolors.qualitative.Bold_9.mpl_colormap(m)
    r=ans[0]
    g=ans[1]
    b=ans[2]
    paint(t)
    gui.set_image(canvas)
    gui.show()