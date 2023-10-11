import taichi as ti
def map_value_to_color(value):#最简单的插值函数
   
    c1 = (1, 0, 0)  # 蓝色
    c2 = (0, 1, 0)  # 绿色
    c3 = (0, 0, 1)  # 红色
    
    if value < 0.5:
        v = 2 * value
        r = c1[0] + (c2[0] - c1[0]) * v
        g = c1[1] + (c2[1] - c1[1]) * v
        b = c1[2] + (c2[2] - c1[2]) * v
    else:
        v = 2 * (value - 0.5)
        r = c2[0] + (c3[0] - c2[0]) * v
        g = c2[1] + (c3[1] - c2[1]) * v
        b = c2[2] + (c3[2] - c2[2]) * v
    
    return (r, g, b)

print(ti.sqrt(2)*ti.sqrt((1-0.5)**2+(1-0.5)**2))
print(map_value_to_color(1.00002))



