import matplotlib.pyplot as plt
import cv2 as cv
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]


class BitPlane_Slicing_Rebuild:

    def __init__(self, img):
        self.img = img

    def getslicing_8_all(self):
        # 8比特图像平面分解
        img_8 = []
        height, width = self.img.shape
        for i in range(8):
            img_8.append(self.img.copy())
        for i in range(height):
            for j in range(width):
                pix = self.img[i, j]
                # 转二进制 并去掉'0b'
                bi_pix = bin(pix)[2:]
                # 右对齐
                bi_pix = bi_pix.rjust(8, '0')
                for n in range(len(bi_pix)):
                    img_8[7 - n][i, j] = int(bi_pix[n])
        return img_8

    def getslicing_pos(self, pos):
        # 获取某一比特平面 pos为第一平面 至 第八平面
        img_pos = self.img.copy()
        height, width = self.img.shape
        for i in range(height):
            for j in range(width):
                temp = self.img[i, j] // int(pow(2, pos - 1))
                if temp == 0 or temp % 2 == 0:
                    img_pos[i, j] = 0
                else:
                    img_pos[i, j] = 1
        return img_pos

    def rebuild_slicing_8(self, img_8):
        # 从比特平面重构图像
        img_re = img_8[0].copy()
        height, width = img_re.shape
        for i in range(height):
            for j in range(width):
                bisum = 0
                for n in range(8):
                    bisum = bisum + img_8[n][i, j] * int(pow(2, n))
                img_re[i, j] = bisum
        return img_re

    def showsclicing(self, imglist):
        # 显示原图像和比特分层图像
        pos = 0
        fig, axe = plt.subplots(nrows=3, ncols=3)
        plt.suptitle("比特分层", fontsize=12)
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

    def show_2pic(self, imgs, imgtitles, maintitle):
        # 显示两张图片 用于对比
        fig, axe = plt.subplots(nrows=1, ncols=2)
        plt.suptitle(maintitle, fontsize=12)
        for i in range(len(imgs)):
            axe[i].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
            axe[i].set_title(imgtitles[i], fontsize=10)
            axe[i].axis(False)
        plt.tight_layout()
        plt.show()


def check_getslicing_8_all(img):
    # 测试比特平面分层函数
    BSR = BitPlane_Slicing_Rebuild(img)
    img_8 = BSR.getslicing_8_all()
    imglist = img_8.copy()
    imglist.insert(0, img)
    BSR.showsclicing(imglist)


def main_getslicing_8_all():
    img1 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    check_getslicing_8_all(img1)


def check_rebuild_slicing_8(img):
    # 测试比特重建函数
    BSR = BitPlane_Slicing_Rebuild(img)
    img_8 = BSR.getslicing_8_all()
    img_re = BSR.rebuild_slicing_8(img_8)
    imgs = [img, img_re]
    imgtitles = ["原图像", "使用比特重建后的图像"]
    maintitle = "从比特平面重建图像"
    BSR.show_2pic(imgs, imgtitles, maintitle)


def main_rebuild_slicing_8():
    img1 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    check_rebuild_slicing_8(img1)


if __name__ == "__main__":
    main_getslicing_8_all()
    main_rebuild_slicing_8()
