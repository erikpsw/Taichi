import taichi as ti
import numpy as np

ti.init(arch=ti.gpu)
LEFT=ti.Vector([1.,0.,0.])
RIGHT=ti.Vector([-1.,0.,0.])
UP=ti.Vector([0.,1.,0.])
DOWN=ti.Vector([0.,-1.,0.])
FRONT=ti.Vector([0.,0.,-1.])
BACK=ti.Vector([0.,0.,1.])

fov=np.pi/3
u=100#一个单位所对应的像素值
camera_distance=5*u#相机距离
canvas_ratio=1#高宽比
canvas_height=round(camera_distance*np.tan(fov/2))
canvas_width=canvas_height*canvas_ratio
camera_pos=ti.Vector([canvas_width/2,canvas_height/2,-camera_distance],ti.f32)
canvas=ti.Vector.field(3, dtype=ti.f32, shape=(canvas_width, canvas_height))#三通道的画布
wall_distance=3*u

#空间矩形
rect_width=2*u
rect_height=canvas_height
rect_pos=ti.Vector([canvas_width/2,canvas_height/2,3*u])#中心点位置
rect_normal=ti.Vector([1.,0.,0.])

@ti.func
def plane_hit_point(start_pos,ray_dir,plane_pos,plane_normal):
    nume=0.
    deno=0.
    for i in ti.static(range(3)):#三个分量
        nume+=(plane_pos[i]-start_pos[i])*plane_normal[i]
        deno+=ray_dir[i]*plane_normal[i]
    return nume/deno

@ti.func
def change_axes(vec,i_hat,j_hat):
    list=[i_hat,j_hat]
    A=ti.Matrix([[0.,0.],[0.,0.]])#三维变二维，要非零
    if(list[0][2]==0):
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                ip=temp[i]
                jp=temp[j]
                A[j,i]+=list[jp][ip]
    elif(list[0][1]==0):
        temp=[0,2]
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                ip=temp[i]
                jp=temp[j]
                A[j,i]+=list[jp][ip]
    else:   
        temp=range(1,3)
        for i in ti.static(range(2)):
            for j in ti.static(range(2)):
                A[j,i]+=list[temp[j]][temp[i]]
    return ti.solve(A,vec[:2])

i_hat=ti.Vector([0,1.,-1.]).normalized()
rect_pos=ti.Vector([0.,canvas_height/2,wall_distance/2])
color=ti.Vector([1.0, 1.0, 1.0])
@ti.kernel
def render():
    for i,j in canvas:
        ray_dir=ti.Vector([i,j,0.])-camera_pos
        t=plane_hit_point(camera_pos,ray_dir,rect_pos,rect_normal)
        point_pos=camera_pos+t*ray_dir
        j_hat=ti.math.cross(rect_normal,i_hat).normalized()
        vec=point_pos-rect_pos
        pos_temp=change_axes(vec,i_hat,j_hat)#使用基向量变换
        if(ti.abs(pos_temp[0])<=rect_width/2 and ti.abs(pos_temp[1])<=rect_height/2):
            canvas[i,j]= color
        else:
            canvas[i,j]= ti.Vector([0, 0., 0.])

gui = ti.GUI("Ray Tracing", res=(canvas_width, canvas_height))
canvas.fill(0)
cnt = 0

while gui.running:
    #左壁
    render()
    # cnt += 1
    # gui.set_image(np.sqrt(canvas.to_numpy() / cnt))#平滑化
    gui.set_image(canvas.to_numpy())
    gui.show()
