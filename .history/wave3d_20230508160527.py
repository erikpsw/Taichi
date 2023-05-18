import taichi as ti
import numpy as np

dt=0.01
width=1200
rotvec = np.array([0., 0.3, 0.])*dt # a single rotation vector
ti.init(arch=ti.cuda)
N = 10

line_points=ti.Vector.field(3,dtype=ti.f32,shape=8)

line_points.from_numpy(
    np.array([
    [-0.5, -0.5, 0.5],   # 0
    [0.5, -0.5, 0.5],    # 1
    [0.5, 0.5, 0.5],     # 2
    [-0.5, 0.5, 0.5],    # 3
    [-0.5, -0.5, -0.5],  # 4
    [0.5, -0.5, -0.5],   # 5
    [0.5, 0.5, -0.5],    # 6
    [-0.5, 0.5, -0.5]    # 7
])
)


window = ti.ui.Window("Rotation", (width, width))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera.position(2, 2, 2)
camera.lookat(-1,-1,-1)


while window.running:
    
    camera.track_user_inputs(window, movement_speed=0.01, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    scene.ambient_light((0.8, 0.8, 0.8))
    
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))

    scene.lines(line_points, color = (0.28, 0.68, 0.99), width = 5.0)
    # Draw 3d-lines in the scene
    canvas.scene(scene)
    window.show()