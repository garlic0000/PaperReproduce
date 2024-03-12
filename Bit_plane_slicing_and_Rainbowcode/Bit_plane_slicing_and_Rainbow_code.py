import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage import util
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]

# 基于比特平面分层和彩虹伪彩色编码的红外图像增强方法
# 比特分层
# 比特层对换
# 灰度转彩色

def getslicing_all(img):
    # 8比特图像平面分解
    img_8 = []
    for i in range(8):
        img_8.append(img.copy())
    for i in range(len(img)):
        for j in range(len(img[0])):
            pix = img[i, j]
            bi_pix = bin(pix)[2:]
            bi_pix = bi_pix.rjust(8, '0')
            for n in range(len(bi_pix)):
                img_8[7 - n][i, j] = int(bi_pix[n])
    return img_8


def changeslicing1(img_8):
    # 高4层和低4层比特平面互换
    # 对换策略?
    # 此函数使用第1层与第8层对换
    img_change = img_8.copy()
    for i in range(4):
        temp = img_change[i].copy()
        img_change[i] = img_change[7 - i].copy()
        img_change[7 - i] = temp.copy()
    return img_change


def changeslicing2(img_8):
    # 高4层和低4层比特平面互换
    # 对换策略?
    # 此函数使用第1层与第5层对换
    img_change = img_8.copy()
    for i in range(4):
        temp = img_change[i].copy()
        img_change[i] = img_change[i + 4].copy()
        img_change[i + 4] = temp.copy()
    return img_change


def rebuild_slicing(img_8):
    # 重构图像
    img_re = img_8[0].copy()
    width = len(img_8[0])
    height = len(img_8[0][0])
    for i in range(width):
        for j in range(height):
            bisum = 0
            for n in range(8):
                bisum = bisum + img_8[n][i, j] * int(pow(2, n))
            img_re[i, j] = bisum
    return img_re


def getpixnumlist(img):
    # 获取像素频数列表
    width, height = img.shape
    pixnumlist = []
    for i in range(256):
        pixnumlist.append(0)
    for i in range(width):
        for j in range(height):
            pix = img[i, j]
            pixnumlist[pix] = pixnumlist[pix] + 1
    return pixnumlist


def get_totalnum(pixnumlist, Lmin, Lmax):
    # 获取指定区域像素范围的像素个数
    totalnum = 0
    for i in range(Lmin, Lmax + 1):
        totalnum = totalnum + pixnumlist[i]
    return totalnum


def get_pk_mk_area(pixnumlist, Lmin, Lmax):
    # 获取指定区域的灰度级k的概率之和pk列表
    # 灰度级k的累加均值mk列表
    totalnum = get_totalnum(pixnumlist, Lmin, Lmax)
    pk = []
    mk = []
    for i in range(256):
        pk.append(0)
        mk.append(0)
    p = 0
    m = 0
    for k in range(Lmin, Lmax + 1):
        percent = pixnumlist[k] / totalnum
        p = p + percent
        pk[k] = p
        m = m + k * percent
        mk[k] = m
    return pk, mk


def getT_area(pixnumlist, Lmin, Lmax):
    # 获取某个像素区间的阈值
    pk, mk = get_pk_mk_area(pixnumlist, Lmin, Lmax)
    maxk = 0
    maxrou_square = 0
    for k in range(Lmin, Lmax + 1):
        p1 = pk[k]
        p2 = pk[Lmax] - p1
        if p1 == 0 or p2 == 0:
            rou_square = 0
        else:
            m1 = 1 / p1 * mk[k]
            m2 = 1 / p2 * (mk[Lmax] - mk[k])
            rou_square = p1 * (m1 - mk[Lmax]) * (m1 - mk[Lmax]) + p2 * (m2 - mk[Lmax]) * (m2 - mk[Lmax])
        if rou_square > maxrou_square:
            maxrou_square = rou_square
            maxk = k
    return maxk


def get_minp_maxp(pixnumlist, Lmin, Lmax):
    # 获取图像中灰度的最小值最大值
    if (Lmin < 0 or Lmin > 255) or (Lmax < 0 or Lmax > 255) or (Lmin > Lmax):
        exit("给定的像素范围有问题")
    minpos = -1
    maxpos = 256
    for i in range(Lmin, Lmax + 1):
        if pixnumlist[i] != 0:
            minpos = i
            break
    for i in range(Lmax, Lmin - 1, -1):
        if pixnumlist[i] != 0:
            maxpos = i
            break
    return minpos, maxpos


def getTs(img):
    pixnumlist = getpixnumlist(img)
    k0, k4 = get_minp_maxp(pixnumlist, 0, 255)
    k2 = getT_area(pixnumlist, k0, k4)
    k1 = getT_area(pixnumlist, k0, k2)
    k3 = getT_area(pixnumlist, k2, k4)
    Ts = [k0, k1, k2, k3, k4]
    return Ts


def binarization(img, T):
    # 根据阈值T 将图像进行二值化
    img_change = img.copy()
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i, j] > T:
                img_change[i, j] = 255
            else:
                img_change[i, j] = 0
    return img_change


def gray_to_red(Ks):
    # 灰色图像进行红色变换 查找表
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
            table_r[r] = (255 - 0) / (k3 - k2) * (r - k2)
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
            table_g[r] = (0 - 255) / (k1 - k0) * (r - k1)
        elif k1 <= r < k2:
            table_g[r] = (255 - 0) / (k2 - k1) * (r - k1)
        elif k2 <= r < k3:
            table_g[r] = (0 - 255) / (k3 - k2) * (r - k3)
        else:
            table_g[r] = (255 - 0) / (k4 - k3) * (r - k3)
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
            table_b[r] = (0 - 255) / (k2 - k1) * (r - k2)
        else:
            table_b[r] = 0
    return table_b


def gray_trans(img_gray, table_color):
    # 通过查找表对灰度图像进行变换
    width, height = img_gray.shape
    img_c = img_gray.copy()
    for i in range(width):
        for j in range(height):
            img_c[i, j] = table_color[img_gray[i, j]]
    return img_c


def gray_to_3singal(img_gray, Ks):
    # 将灰度图像转为三个单通道图像
    table_r = gray_to_red(Ks)
    table_g = gray_to_green(Ks)
    table_b = gray_to_blue(Ks)
    img_r = gray_trans(img_gray, table_r)
    img_g = gray_trans(img_gray, table_g)
    img_b = gray_trans(img_gray, table_b)
    return img_r, img_g, img_b


def grays_to_color(img_r, img_g, img_b):
    # 将三个单通道图像合成为伪彩色图像
    pix = []
    width, height = img_r.shape
    img_rgb = np.zeros((width, height, 3))
    for i in range(width):
        for j in range(height):
            pix.append(img_r[i, j])
            pix.append(img_g[i, j])
            pix.append(img_b[i, j])
            img_rgb[i, j] = pix.copy()
            pix.clear()
    img_rgb = img_rgb.astype(np.uint8)
    return img_rgb


def smooth_cv():
    img = cv.imread("../Picture/cloud1.jpg", cv.IMREAD_GRAYSCALE)
    img_noise = util.random_noise(img, mode='gaussian', var=0.01)
    img_noise = util.img_as_ubyte(img_noise)
    # 双边滤波
    img_result1 = cv.bilateralFilter(img_noise, d=9, sigmaColor=50, sigmaSpace=100)
    # 3×3均值滤波
    img_result2 = cv.blur(img_noise, ksize=(3, 3))
    # 15×15均值滤波
    img_result3 = cv.blur(img_noise, ksize=(15, 15))
    # 3×3高斯滤波
    img_result4 = cv.GaussianBlur(img_noise, (3, 3), sigmaX=0, sigmaY=0)
    # 15×15高斯滤波
    img_result5 = cv.GaussianBlur(img_noise, (15, 15), sigmaX=0, sigmaY=0)

    plt.figure(figsize=(25, 12))
    plt.gray()
    plt.suptitle("使用OpenCV进行图像平滑", fontdict={'size': 15})

    plt.subplot(2, 4, 1)
    plt.imshow(img, vmin=0, vmax=255)
    plt.title("原图", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 2)
    plt.imshow(img_noise, vmin=0, vmax=255)
    plt.title("添加高斯噪声的图像", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 3)
    plt.imshow(img_result1, vmin=0, vmax=255)
    plt.title("双边滤波", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 4)
    plt.imshow(img_result2, vmin=0, vmax=255)
    plt.title("3×3均值滤波", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 5)
    plt.imshow(img_result3, vmin=0, vmax=255)
    plt.title("15×15均值滤波", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 6)
    plt.imshow(img_result4, vmin=0, vmax=255)
    plt.title("3×3高斯滤波", fontdict={'size': 15})
    plt.axis(False)

    plt.subplot(2, 4, 7)
    plt.imshow(img_result5, vmin=0, vmax=255)
    plt.title("15×15高斯滤波", fontdict={'size': 15})
    plt.axis(False)

    plt.show()


def showsclicing(imglist):
    # 显示比特分层图像
    pos = 0
    fig, axe = plt.subplots(nrows=3, ncols=3)
    axe[0, 0].imshow(imglist[0], cmap='gray', vmin=0, vmax=255)
    axe[0, 0].set_title("原图像", fontsize=10)
    axe[0, 0].axis(False)
    for i in range(3):
        for j in range(3):
            if i == 0 and j == 0:
                pos = pos + 1
                continue
            axe[i, j].imshow(imglist[pos], cmap='gray', vmin=0, vmax=1)
            axe[i, j].set_title("第{}平面".format(pos), fontsize=10)
            axe[i, j].axis(False)
            pos = pos + 1
    plt.tight_layout()
    plt.show()


def checkchangeslicing():
    img = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    img_8 = getslicing_all(img)
    imglist = img_8.copy()
    imglist.insert(0, img)
    showsclicing(imglist)
    imgchange = changeslicing1(img_8)
    img_ch_re = rebuild_slicing(imgchange)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.title("原图像", fontsize=10)
    plt.axis(False)
    plt.subplot(1, 2, 2)
    plt.imshow(img_ch_re, cmap='gray', vmin=0, vmax=255)
    plt.title("对调比特平面", fontsize=10)
    plt.axis(False)
    plt.tight_layout()
    plt.show()


def check():
    img = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    # img = cv.imread("../Picture/dark_lingxiaohua1.jpg", cv.IMREAD_GRAYSCALE)
    # img = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    # img = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    # img = cv.imread("../Picture/cat1.jpg", cv.IMREAD_GRAYSCALE)
    img_8 = getslicing_all(img)  # 获取所有比特平面
    img_change = changeslicing1(img_8)  # 比特平面对调
    img_rebuild = rebuild_slicing(img_change)  # 将比特平面重构为图像
    Ts = getTs(img_rebuild)
    img_r, img_g, img_b = gray_to_3singal(img_rebuild, Ts)
    img_rgb = grays_to_color(img_r, img_g, img_b)
    img_result1 = cv.bilateralFilter(img_rebuild, d=9, sigmaColor=50, sigmaSpace=100)
    img_result2 = cv.blur(img_rebuild, ksize=(5, 5))
    img_result3 = cv.GaussianBlur(img_rebuild, (5, 5), sigmaX=0, sigmaY=0)
    imgs = [img, img_rebuild, img_result1, img_result2, img_result3, img_rgb]
    imgtitle = ["原图像", "比特平面对换后的图像", "双边滤波处理后的图像",
                "均值滤波处理后的图像", "高斯滤波处理后的图像", "伪彩色增强后的图像"]
    pos = 0
    fig, axe = plt.subplots(nrows=2, ncols=3)
    for i in range(2):
        for j in range(3):
            axe[i, j].imshow(imgs[pos], cmap='gray', vmin=0, vmax=255)
            axe[i, j].set_title(imgtitle[pos], fontsize=10)
            axe[i, j].axis(False)
            pos = pos + 1
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # checkchangeslicing()
    check()
