import taichi as ti
import numpy as np

dt=0.01
width=1200
rotvec = np.array([0., 0.3, 0.])*dt # a single rotation vector
ti.init(arch=ti.cuda)
N = 300
points=ti.Vector.field(3,dtype=ti.f32,shape=N*N)
canvas=ti.Vector.field(3,dtype=ti.f32,shape=N*N)
X,Y=np.linspace(0,1,N),np.linspace(0,1,N)
h_field=[]
h=0.3

for i in range(N):
    for j in range(N):
        h_field.append([X[i],h,Y[j]])
points.from_numpy(
    np.array(h_field)
)


window = ti.ui.Window("Rotation", (width, width))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera.position(2, 2, 2)
camera.lookat(-1,-1,-1)
@ti.func
def get_h(A,x0,y0,x,y,lam,w,t,p0):
    d=np.sqrt((x-x0)**2+(y-y0)**2)
    return(A*np.cos(w*t-(2*np.pi*d/lam)+p0))
t=5
for i in range(N*N):
    points[i][1]=get_h(0.2,0.3,0.3,points[i][0],points[i][2],0.2,0.5,t,0)+get_h(0.15,0.7,0.7,points[i][0],points[i][2],0.2,0.5,t,0)
while window.running:
    camera.track_user_inputs(window, movement_speed=0.01, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    scene.ambient_light((0.8, 0.8, 0.8))
    
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))
    scene.particles(points, color = (0.28, 0.68, 0.99),radius=0.005)
    # Draw 3d-lines in the scene
    canvas.scene(scene)
    window.show()