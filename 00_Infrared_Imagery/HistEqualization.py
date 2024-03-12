import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]


def getpixnumlist(img):
    # 获取像素频数列表
    height, width = img.shape
    pixnumlist = []
    for i in range(256):
        pixnumlist.append(0)
    for i in range(height):
        for j in range(width):
            pix = img[i, j]
            pixnumlist[pix] = pixnumlist[pix] + 1
    return pixnumlist


def getpixpercentlist(img):
    # 获取像素频率列表
    height, width = img.shape
    totalnum = height * width
    pixnumlist = getpixnumlist(img)
    pixpercentlist = np.zeros(len(pixnumlist))
    for i in range(len(pixnumlist)):
        pixpercentlist[i] = pixnumlist[i] / totalnum
    return pixpercentlist


def get_pk_list(img):
    # 获取像素频率的累积和
    pixpercent = getpixpercentlist(img)
    pk = []
    p = 0
    for i in range(len(pixpercent)):
        p = p + pixpercent[i]
        pk.append(p)
    return pk


def Equalization(img):
    # 直方图均衡化
    img_e = img.copy()
    pr = get_pk_list(img)
    height, width = img_e.shape
    for i in range(height):
        for j in range(width):
            # 四舍五入
            img_e[i, j] = int(255 * pr[img[i, j]] + 0.5)
    return img_e


def show_pic_hist(imgs, imgtitles, maintitle):
    # 显示图像及其直方图
    x_pix = []
    for i in range(256):
        x_pix.append(i)
    fig, axe = plt.subplots(nrows=len(imgs), ncols=3)
    plt.suptitle(maintitle, fontsize=15)
    for i in range(len(imgs)):
        axe[i, 0].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
        axe[i, 0].set_title(imgtitles[i], fontsize=10)
        axe[i, 0].axis(False)
        pixnumlist = getpixnumlist(imgs[i])
        pixpercentlist = getpixpercentlist(imgs[i])
        axe[i, 1].bar(x_pix, pixnumlist)
        axe[i, 2].bar(x_pix, pixpercentlist)
    plt.tight_layout()
    plt.show()


def check_qualization(img):
    # 测试函数
    img_e = Equalization(img)
    imgs = [img, img_e]
    imgtitles = ["原图像", "进行直方图均衡化后的图像"]
    maintitle = ""
    show_pic_hist(imgs, imgtitles, maintitle)


def main_qualization():
    img1 = cv.imread("../Picture/lingxiaohua.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img4 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_qualization(img1)
    check_qualization(img2)
    check_qualization(img3)
    check_qualization(img4)


if __name__ == "__main__":
    main_qualization()
