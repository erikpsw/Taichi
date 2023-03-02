import taichi as ti
import numpy as np

ti.init(arch=ti.cuda)

N = 10

vertices=ti.field(shape=24,dtype=ti.f32)
indices=ti.field(shape=36,dtype=ti.int32)
indices.from_numpy(np.array([2 ,1 , 4,
4 ,7 ,2,

# 后面（Z轴正向）
    6 ,4 ,1,
    1 ,2 ,6,

    # 左面（X轴负向）
    7 ,4 ,6,
    6 ,2 ,7,

    # 右面（X轴正向）
    1 ,4 ,6,
    6 ,2 ,1,

    # 上面（Y轴正向）
    7 ,2 ,6,
    6 ,4 ,7,

    # 下面（Y轴负向）
    1 ,4 ,7,
    7 ,2 ,1]))


for i in range(24):
    vertices[i] =[-0.5, -0.5, -0.5, # 0
            0.5, -0.5, -0.5, # 1
            0.5, 0.5, -0.5, # 2
            -0.5, 0.5, -0.5, # 3
            -0.5, -0.5, 0.5, # 4
            0.5, -0.5, 0.5, # 5
            0.5, 0.5, 0.5,#6 
            -0.5,-0.5,-0.5][i]



window = ti.ui.Window("Test for Drawing 3d-lines", (768, 768))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()
camera.position(4, 2, 2)

while window.running:
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
    scene.set_camera(camera)
    scene.ambient_light((0.8, 0.8, 0.8))
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(1, 1, 1))

    scene.mesh(vertices, indices, color = (0.28, 0.68, 0.99))
    # Draw 3d-lines in the scene
    canvas.scene(scene)
    window.show()