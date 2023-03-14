import taichi as ti
import numpy as np
from scipy.spatial.transform import Rotation

dt=0.01
width=1200
rotvec = np.array([0., 0.3, 0.])*dt # a single rotation vector
rotation = Rotation.from_rotvec(rotvec) # create a rotation object
ti.init(arch=ti.cuda)
N = 10

vertices=ti.Vector.field(3,dtype=ti.f32,shape=8)
indices=ti.field(shape=36,dtype=ti.int32)
indices.from_numpy(np.array( [[0, 1, 2],  # 前面
    [0, 2, 3],
    [1, 5, 6],  # 右侧
    [1, 6, 2],
    [5, 4, 7],  # 后面
    [5, 7, 6],
    [4, 0, 3],  # 左侧
    [4, 3, 7],
    [3, 2, 6],  # 顶面
    [3, 6, 7],
    [1, 0, 4],  # 底面
    [1, 4, 5]]).reshape(-1))
vertices.from_numpy(
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
    vertices.from_numpy(rotation.apply(vertices.to_numpy()))
    scene.set_camera(camera)
    scene.ambient_light((0.8, 0.8, 0.8))
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))

    scene.mesh(vertices, indices, color = (0.28, 0.68, 0.99))
    # Draw 3d-lines in the scene
    canvas.scene(scene)
    window.show()