import taichi as ti
ti.init()

N = 10
dt = 5e-5

pos = ti.Vector.var(2, ti.f32, N, needs_grad=True)
#点的位置
vel = ti.Vector.var(2, ti.f32, N)
#速度矢量
potential = ti.var(ti.f32, (), needs_grad=True)
#允许微分


@ti.kernel
def calc_potential():#计算势能
    for i, j in ti.ndrange(N, N):
        disp = pos[i] - pos[j]#两点的向量
        potential[None] += 1 / disp.norm(1e-3)


@ti.kernel
def init():
    for i in pos:
        pos[i] = [ti.random(), ti.random()]
#随机初始化

@ti.kernel
def advance():
    for i in pos:
        vel[i] += dt * pos.grad[i]
        #位置的一阶导数
    for i in pos:
        pos[i] += dt * vel[i]
        #局部线性化，看成匀速


def substep():
    with ti.Tape(potential):
        calc_potential()
    advance()


init()
gui = ti.GUI('Autodiff gravity')
while gui.running and not gui.get_event(gui.ESCAPE):
    for i in range(16):
        substep()
    gui.circles(pos.to_numpy(), radius=3)
    #画一个实心圆（点）
    gui.show()
