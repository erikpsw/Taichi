import numpy as np
import taichi as ti
ti.init(ti.gpu)


def get_dir():
    t=np.random.rand()
    if(t<=0.25):
        return[-1,0]
    elif(t>0.25 and t<=0.5):
        return[0,1]
    elif(t>0.5 and t<=0.75):
        return[1,0]   
    elif(t>0.75):
        return[0,-1]
canvas_width=512
pos=[canvas_width/2,canvas_width/2]
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_width))#三通道的画布

gui=ti.GUI("random walk",(canvas_width,canvas_width))
while gui.running:
    canvas[pos[0],pos[1]]+=ti.Vector([1.,1.,1.])
    gui.show()