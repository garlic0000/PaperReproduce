import numpy as np


def gray_to_red(Ks):
    # 灰色图像进行红色变 查找表
    k0 = Ks[0]
    k2 = Ks[2]
    k3 = Ks[3]
    table_r = []
    for i in range(256):
        table_r.append(0)
    for r in range(256):
        if k0 <= r < k2:
            table_r[r] = 0
        elif k2 <= r < k3:
            table_r[r] = ((255 - 0) /
                          (k3 - k2) * (r - k2))
        else:
            table_r[r] = 255
    return table_r


def gray_to_green(Ks):
    # 灰色图像进行绿色变换 查找表
    k0 = Ks[0]
    k1 = Ks[1]
    k2 = Ks[2]
    k3 = Ks[3]
    k4 = Ks[4]
    table_g = []
    for i in range(256):
        table_g.append(0)
    for r in range(256):
        if k0 <= r < k1:
            table_g[r] = ((0 - 255)
                          / (k1 - k0) * (r - k1))
        elif k1 <= r < k2:
            table_g[r] = ((255 - 0)
                          / (k2 - k1) * (r - k1))
        elif k2 <= r < k3:
            table_g[r] = ((0 - 255)
                          / (k3 - k2) * (r - k3))
        else:
            table_g[r] = ((255 - 0)
                          / (k4 - k3) * (r - k3))
    return table_g


def gray_to_blue(Ks):
    # 灰色图像进行蓝色变换 查找表
    k0 = Ks[0]
    k1 = Ks[1]
    k2 = Ks[2]
    table_b = []
    for i in range(256):
        table_b.append(0)
    for r in range(256):
        if k0 <= r < k1:
            table_b[r] = 255
        elif k1 <= r < k2:
            table_b[r] = ((0 - 255)
                          / (k2 - k1) * (r - k2))
        else:
            table_b[r] = 0
    return table_b


