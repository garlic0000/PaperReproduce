import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]


# 为什么平滑可以消除噪声
# 为什么低位受噪声的影响更大
# 为什么取均值或者中值 可以使图像变得平滑
def getslicing_all(img):
    img_8 = []
    for i in range(8):
        img_8.append(img.copy())
    width, height = img.shape
    for i in range(width):
        for j in range(height):
            pix = img[i, j]
            pix_bi = bin(pix)[2:]
            pix_bi = pix_bi.rjust(8, '0')
            for n in range(8):
                img_8[7 - n][i, j] = int(pix_bi[n])
    return img_8


def rebuild_slicing_low4(img_8):
    # 只将低4个比特进行合成
    width, height = img_8[0].shape
    img_re_low4 = img_8[0].copy()
    for i in range(width):
        for j in range(height):
            pixnum = 0
            for n in range(4):
                pixnum = pixnum + img_8[n][i, j] * int(pow(2, n))
            img_re_low4[i, j] = pixnum

    return img_re_low4


def mean_filter(img, m):
    # 均值滤波 m×m为滤波盒的尺寸
    # 填充0
    width, height = img.shape
    img_expand = np.zeros((width + m // 2, height + m // 2))
    for i in range(m // 2, width + m // 2):
        for j in range(m // 2, height + m // 2):
            img_expand[i, j] = img[i - m // 2, j - m // 2]
    img_mean = img.copy()
    for i in range(m // 2, width + m // 2):
        for j in range(m // 2, height + m // 2):
            # 滤波盒均值运算
            sum_pix = 0
            for p in range(i - m // 2, i + m // 2):
                for q in range(j - m // 2, j + m // 2):
                    sum_pix = sum_pix + img_expand[p, q]
            ave_pix = sum_pix // (m * m)
            img_mean[i - m // 2, j - m // 2] = ave_pix
    return img_mean


def copyfill(img, m):
    img_middle = img.copy()
    height, width = img_middle.shape
    # 将图像周围m//2行和列复制一周
    img_expand = np.zeros((height + (m // 2) * 2, width + (m // 2) * 2))
    # 中间为原数组
    for i in range(m // 2, height + m // 2):
        for j in range(m // 2, width + m // 2):
            img_expand[i, j] = img_middle[i - m // 2, j - m // 2].copy()
    # 左边
    for i in range(m // 2, height + m // 2):
        for j in range(0, m // 2):
            img_expand[i, j] = img_expand[i, j + m // 2].copy()
    # 右边
    for i in range(m // 2, height + m // 2):
        for j in range(width + m // 2, width + (m//2)*2):
            img_expand[i, j] = img_expand[i, j - m // 2].copy()
    # 上边
    for i in range(0, m // 2):
        for j in range(m // 2, width + m // 2):
            img_expand[i, j] = img_expand[i + m // 2, j].copy()
    # 下边
    for i in range(height + m // 2, height + (m//2)*2):
        for j in range(m // 2, width + m // 2):
            img_expand[i, j] = img_expand[i - m // 2, j].copy()
    # 左上角
    for i in range(0, m // 2):
        for j in range(0, m // 2):
            img_expand[i, j] = img_expand[i + m // 2, j + m // 2].copy()
    # 右上角
    for i in range(height + m // 2, height + (m//2)*2):
        for j in range(0, m // 2):
            img_expand[i, j] = img_expand[i - m // 2, j + m // 2].copy()
    # 左下角
    for i in range(0, m // 2):
        for j in range(width + m // 2, width + (m//2)*2):
            img_expand[i, j] = img_expand[i + m // 2, j - m // 2].copy()
    # 右下角
    for i in range(height + m // 2, height + (m//2)*2):
        for j in range(width + m // 2, width + (m//2)*2):
            img_expand[i, j] = img_expand[i - m // 2, j - m // 2].copy()
    return img_expand


# 中值滤波
def middle_filter(img, m):
    img_mf = img.copy()
    img_expand = copyfill(img, m)
    height, width = img.shape
    for i in range(height):
        for j in range(width):
            return 0

    return 0


def add_high(img_mean, img_8):
    # 将高比特平面上的值加入到进行去噪的低比特平面
    width, height = img_mean.shape
    img_add = img_mean.copy()
    for i in range(width):
        for j in range(height):
            pixnum = img_mean[i, j]
            for n in range(4, 8):
                pixnum = pixnum + img_8[n][i, j] * int(pow(2, n))
            img_add[i, j] = pixnum
    return img_add


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


def check():
    # img = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    img = data.coins()
    img_8 = getslicing_all(img)
    img_re_low4 = rebuild_slicing_low4(img_8)
    img_smooth_low4 = mean_filter(img_re_low4, 3)
    img_re = add_high(img_smooth_low4, img_8)
    imgs = [img, img_re]
    imgtitle = ["原图像", "低比特平面去噪处理后的图像"]
    fig, axe = plt.subplots(nrows=1, ncols=2)
    for i in range(2):
        axe[i].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
        axe[i].set_title(imgtitle[i], fontsize=10)
        axe[i].axis(False)
    plt.tight_layout()
    plt.show()

    imglist1 = img_8.copy()
    imglist1.insert(0, img)
    img_8_2 = getslicing_all(img_re)
    imglist2 = img_8_2.copy()
    imglist2.insert(0, img_re)
    showsclicing(imglist1)
    showsclicing(imglist2)


if __name__ == "__main__":
    img_expand = copyfill()
