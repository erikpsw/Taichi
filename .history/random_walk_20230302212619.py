import numpy as np
import taichi as ti
from collections import deque

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
    
path=deque()
canvas_width=512
path_length=10
pixel_size=4
mid=int(canvas_width/(2*pixel_size))
pos=[mid,mid]
canvas=np.zeros((canvas_width,canvas_width,3))

gui=ti.GUI("random walk",(canvas_width,canvas_width))
while gui.running:
    l=len(path)
    if(l==path_length):
        canvas[path[0][0]*pixel_size:path[0][0]*pixel_size+pixel_size,path[0][1]*pixel_size:path[0][1]*pixel_size+pixel_size,:]=[0.,0.,0.]
        path.pop(0)
    path.append(pos)
    for i in range(l):
        canvas[path[l-i-1][0]*pixel_size:path[l-i-1][0]*pixel_size+pixel_size,path[l-i-1][1]*pixel_size:path[l-i-1][1]*pixel_size+pixel_size,:]=[i/l,i/l,i/l]
    dir=get_dir()
    pos[0]+=dir[0]
    pos[1]+=dir[1]
    gui.clear()
    gui.set_image(canvas)
    gui.show()