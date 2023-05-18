import taichi as ti
import numpy as np

dt=0.01
ti.init(arch=ti.cuda)
N = 300
canvas = ti.Vector.field(3, dtype=ti.f64, shape=(N,N))

gui = ti.GUI("Mandelbrot Set", res=(N , N),fast_gui=True)#使gpu用快速渲染
@ti.func
def get_h(A,x0,y0,x,y,lam,w,t,p0):
    d=np.sqrt((x-x0)**2+(y-y0)**2)
    return(A*np.cos(w*t-(2*np.pi*d/lam)+p0))
t=5
A1=0.2
@ti.kernel
def paint():
    for i, j in canvas: 
        canvas[i, j] = ti.Vector([iterations*2 ,255,255])/255

while gui.running:
    camera.track_user_inputs(window, movement_speed=0.01, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    scene.ambient_light((0.8, 0.8, 0.8))
    
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))
    scene.particles(points, color = (0.28, 0.68, 0.99),radius=0.005)
    # Draw 3d-lines in the scene
    canvas.scene(scene)
    window.show()