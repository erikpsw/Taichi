import taichi as ti

ti.init(arch=ti.cuda)

N = 10

vertex=ti.field(shape=24)
indices=ti.field(shape=36)

@ti.kernel
def init_points_pos():
    for i in range(24):
        vertex[i] = 
    for j in range(36):
        indices[i]=


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

    scene.mesh(vertices, indices, normals, color, per_vertex_color)
    # Draw 3d-lines in the scene
    scene.lines(points_pos, color = (0.28, 0.68, 0.99), width = 5.0)
    canvas.scene(scene)
    window.show()