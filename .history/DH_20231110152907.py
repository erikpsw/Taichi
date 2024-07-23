import taichi as ti
ti.init(arch=ti.gpu)
import numpy as np
from math import *
I=0.25

window_width = 600

DH=np.array([
    [0,0,0,90],
    [45,0.16,-0.4,0],
    [0,-0.14,0,90],
    [0,0.45,0,90],
    [0,0,0,-90],
    [0,0.07,0,0]
             ])
x0,y0,z0=0,0,0
pos=np.array([
    [1,0,0,x0],
    [0,1,0,y0],
    [0,0,1,z0],
    [0,0,0,1]
    ])
p_list=[]
for link in DH:
    theta=radians(link[0])
    d=link[1]
    x=link[2]
    alpha=radians(link[3])
    T=np.array([
        [cos(theta),-sin(theta)*cos(theta),sin(theta)*sin(alpha),cos(theta)*x],
        [sin(theta),cos(theta)*cos(alpha),-cos(theta)*sin(alpha),sin(theta)*x],
        [0,sin(alpha),cos(alpha),d],
        [0,0,0,1]
        ])
    pos=pos@T
    p_list.append(pos[:3,3])
# p_list=ti.Vector.field(p_list,dtype=float)
N=len(p_list)
line_points=ti.Vector.field(3,dtype=ti.f32,shape=2*(N-1))
tmp=[]
for i in range(N-1):
    tmp.append(p_list[i])
    tmp.append(p_list[i+1])
line_points.from_numpy(np.array(tmp))

window = ti.ui.Window("Robot", (window_width, window_width))
scene = ti.ui.Scene()
canvas = window.get_canvas()
camera = ti.ui.Camera()
camera.position(2, 2, 2)
camera.lookat(-1,-1,-1)
path=[]

while window.running:
    # print(path)
    # scene.particles(line_points,radius=5,color=0x51acea)
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
    scene.lines(line_points, color = (0.28, 0.68, 0.99), width = 5.0)
    # path.append(n2.pos)
    scene.set_camera(camera)
    canvas.scene(scene)
    window.show()


