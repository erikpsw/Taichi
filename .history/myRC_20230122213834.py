import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)

fov=np.pi/3
camera_distance=100#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio


