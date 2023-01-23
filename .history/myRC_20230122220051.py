import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)

fov=np.pi/3
u=100#一个单位所对应的像素值
camera_distance=5*u#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_height))#三通道的画布

#矩形
rect_width=u
rect_height=u
pos=ti.Vector([canvas_width/2,canvas_height/2,u])
for i,j in canvas:
    canvas[i,j]= [0, 0, 0]

gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)
cnt = 0
while gui.running:
    # cnt += 1
    # gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.set_image(canvas.to_numpy())
    gui.show()
