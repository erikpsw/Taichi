import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)

fov=np.pi/3
u=100#一个单位所对应的像素值
camera_distance=5*u#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio
camera_pos=ti.Vector([canvas_width/2,canvas_height/2,-camera_distance],dtype=ti.f32)
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_height))#三通道的画布

#空间矩形
rect_width=u
rect_height=u
rect_pos=ti.Vector([canvas_width/2,canvas_height/2,3*u])#中心点位置
rect_normal=ti.Vector([0.,0.,1.])

@ti.func
def plane_hit_point(start_pos,ray_dir,plane_pos,plane_normal):
    nume=0
    deno=0
    for i in ti.static(range(3)):#三个分量
        nume+=(plane_pos[i]-start_pos[i])*plane_normal[i]
        deno+=ray_dir[i]*plane_normal[i]
    return nume/deno

@ti.kernel
def render():
    for i,j in canvas:
        ray_dir=ti.Vector([i,j,0.])-camera_pos
        t=plane_hit_point(camera_pos,ray_dir,rect_pos,rect_normal)
        point_pos=camera_pos+t*ray_dir
        if(point_pos[0]>rect_pos[0]-rect_width/2):
            canvas[i,j]= ti.Vector([1., 0., 0.])
        else:
            canvas[i,j]= ti.Vector([0, 0., 0.])

gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)
cnt = 0

while gui.running:
    render()
    # cnt += 1
    # gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.set_image(canvas.to_numpy())
    gui.show()
