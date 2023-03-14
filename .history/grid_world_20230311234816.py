import taichi as ti
import numpy as np

ti.init(ti.cuda)
pixel_size=40
canvas_width=10
canvas_width=10
canvas=np.zeros((canvas_width,canvas_width,3))

while gui.running:
    l=len(path)
    if(l>=path_length):
        canvas[path[0][0]*pixel_size:path[0][0]*pixel_size+pixel_size,path[0][1]*pixel_size:path[0][1]*pixel_size+pixel_size,:]=[0.,0.,0.]
        path.popleft()
    path.append([pos[0],pos[1]])
    for i in range(l):
        # canvas[path[l-i-1][0]*pixel_size:path[l-i-1][0]*pixel_size+pixel_size,path[l-i-1][1]*pixel_size:path[l-i-1][1]*pixel_size+pixel_size,:]=[1-i/l,1-i/l,1-i/l]
        canvas[path[l-i-1][0]*pixel_size:(path[l-i-1][0]+1)*pixel_size,path[l-i-1][1]*pixel_size:(path[l-i-1][1]+1)*pixel_size]=[1.,1.,1.]
    dir=get_dir()
    pos[0]+=dir[0]
    pos[1]+=dir[1]
    gui.set_image(canvas)
    gui.show()