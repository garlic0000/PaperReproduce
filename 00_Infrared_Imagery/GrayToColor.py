import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import RainbowCode_T
import RainbowCode
import GetThreshold


def gray_trans(img_gray, table_color):
    # 通过查找表对灰度图像进行变换
    height, width = img_gray.shape
    img_c = img_gray.copy()
    for i in range(height):
        for j in range(width):
            img_c[i, j] = table_color[img_gray[i, j]]
    return img_c


def gray_to_3singal_T(img_gray, Ks):
    # 将灰度图像转为三个单通道图像
    table_r = RainbowCode_T.gray_to_red(Ks)
    table_g = RainbowCode_T.gray_to_green(Ks)
    table_b = RainbowCode_T.gray_to_blue(Ks)
    img_r = gray_trans(img_gray, table_r)
    img_g = gray_trans(img_gray, table_g)
    img_b = gray_trans(img_gray, table_b)
    return img_r, img_g, img_b


def gray_to_3singal(img_gray):
    # 将灰度图像转为三个单通道图像
    table_r = RainbowCode.gray_to_red()
    table_g = RainbowCode.gray_to_green()
    table_b = RainbowCode.gray_to_blue()
    img_r = gray_trans(img_gray, table_r)
    img_g = gray_trans(img_gray, table_g)
    img_b = gray_trans(img_gray, table_b)
    return img_r, img_g, img_b


def grays_to_color(img_r, img_g, img_b):
    # 将三个单通道图像合成为伪彩色图像
    pix = []
    height, width = img_r.shape
    img_rgb = np.zeros((height, width, 3))
    for i in range(height):
        for j in range(width):
            pix.append(img_r[i, j])
            pix.append(img_g[i, j])
            pix.append(img_b[i, j])
            img_rgb[i, j] = pix.copy()
            pix.clear()
    img_rgb = img_rgb.astype(np.uint8)
    return img_rgb


def show_2pic(imgs, imgtitles, maintitle):
    # 显示两张图片 用于对比
    fig, axe = plt.subplots(nrows=1, ncols=2)
    plt.suptitle(maintitle, fontsize=12)
    for i in range(len(imgs)):
        axe[i].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
        axe[i].set_title(imgtitles[i], fontsize=10)
        axe[i].axis(False)
    plt.tight_layout()
    plt.show()


def show_4pic_gray(imgs, imgtitles, maintitle):
    # 显示两张图片 用于对比
    fig, axe = plt.subplots(nrows=2, ncols=2)
    plt.suptitle(maintitle, fontsize=12)
    pos = 0
    for i in range(2):
        for j in range(2):
            axe[i, j].imshow(imgs[pos], cmap='gray', vmin=0, vmax=255)
            axe[i, j].set_title(imgtitles[pos], fontsize=10)
            axe[i, j].axis(False)
            pos = pos + 1
    plt.tight_layout()
    plt.show()


def show_4pic_rgb(imgs, imgtitles, maintitle, cmaps):
    # 显示两张图片 用于对比
    fig, axe = plt.subplots(nrows=2, ncols=2)
    plt.suptitle(maintitle, fontsize=12)
    pos = 0
    for i in range(2):
        for j in range(2):
            axe[i, j].imshow(imgs[pos], cmap=cmaps[pos], vmin=0, vmax=255)
            axe[i, j].set_title(imgtitles[pos], fontsize=10)
            axe[i, j].axis(False)
            pos = pos + 1
    plt.tight_layout()
    plt.show()


def check_gray_to_3singal_T(img):
    Ts = GetThreshold.getTs(img)
    img_r, img_g, img_b = gray_to_3singal_T(img, Ts)
    imgs = [img, img_r, img_g, img_b]
    imgtitles = ["原图像", "红色单色图像", "绿色单色图像", "蓝色单色图像"]
    maintitle = ''
    # https://blog.csdn.net/qq_38048756/article/details/118724555
    cmaps = ['gray', 'autumn', 'summer', 'winter']
    show_4pic_gray(imgs, imgtitles, maintitle)
    show_4pic_rgb(imgs, imgtitles, maintitle, cmaps)


def main_gray_to_3signal_T():
    img1 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_gray_to_3singal_T(img1)
    check_gray_to_3singal_T(img2)
    check_gray_to_3singal_T(img3)


def check_grays_to_color(img):
    Ts = GetThreshold.getTs(img)
    img_r, img_g, img_b = gray_to_3singal_T(img, Ts)
    img_rgb = grays_to_color(img_r, img_g, img_b)
    imgs = [img, img_rgb]
    imgtitles = ["原图像", "伪彩色图像"]
    maintitle = ''
    show_2pic(imgs, imgtitles, maintitle)


def main_grays_to_color():
    img1 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_grays_to_color(img1)
    check_grays_to_color(img2)
    check_grays_to_color(img3)


if __name__ == "__main__":
    main_grays_to_color()
