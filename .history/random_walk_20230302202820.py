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
pixel_size=4
mid=int(canvas_width/(2*pixel_size))
pos=[mid,mid]
canvas=np.zeros((int(canvas_width/pixel_size),int(canvas_width/pixel_size),3))

gui=ti.GUI("random walk",(canvas_width,canvas_width))
while gui.running:
    canvas[pos[0]*pixel_size:pos[0]*pixel_size+pixel_size,pos[1]*pixel_size:pos[1]*pixel_size+pixel_size,:]=[1.,1.,1.]
    dir=get_dir()
    pos[0]+=dir[0]
    pos[1]+=dir[1]
    gui.set_image(canvas)
    gui.show()