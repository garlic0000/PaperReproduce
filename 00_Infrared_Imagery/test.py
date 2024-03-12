import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import BitPlane_Slicing_Rebuild
import BitPlane_Change
import GetThreshold
import GrayToColor
import LowBitPlane_Solve


def show(imgs, imgtitles, maintitle, rows, cols):
    # 显示图片
    if rows == 1:
        fig, axe = plt.subplots(nrows=rows, ncols=cols)
        plt.suptitle(maintitle, fontsize=12)
        for i in range(len(imgs)):
            axe[i].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
            axe[i].set_title(imgtitles[i], fontsize=10)
            axe[i].axis(False)
        plt.tight_layout()
        plt.show()
    else:
        pos = 0
        fig, axe = plt.subplots(nrows=rows, ncols=cols)
        plt.suptitle(maintitle, fontsize=12)
        for i in range(rows):
            for j in range(cols):
                if i * rows + j + 1 > len(imgs) or pos >= len(imgs):
                    # 就算不绘制图像 也会有坐标轴
                    axe[i, j].axis(False)
                    break
                axe[i, j].imshow(imgs[pos], cmap='gray', vmin=0, vmax=255)
                axe[i, j].set_title(imgtitles[pos], fontsize=10)
                axe[i, j].axis(False)
                pos = pos + 1
        plt.tight_layout()
        plt.show()


def check_1(img):
    # 测试比特平面对调
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)  # 获取所有比特平面
    img_change = BitPlane_Change.changeslicing_1(img_8)  # 比特平面对调
    img_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_change)  # 将比特平面重构为图像
    imgs = [img, img_rebuild]
    imgtitles = ["原图像", "比特平面对换后的图像"]
    maintitle = "比特平面对调"
    show(imgs, imgtitles, maintitle, rows=1, cols=2)


def main_1():
    # 当图片尺寸很大时 需要很长时间
    # img1 = cv.imread("../Picture/food1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img4 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    # check_1(img1)
    check_1(img2)
    check_1(img3)
    check_1(img4)


def check_2(img):
    # 对图像进行平滑处理后
    # 再进行比特平面对调
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)
    img_change = BitPlane_Change.changeslicing_1(img_8)
    img_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_change)
    img_mean, img_gaussian = LowBitPlane_Solve.smooth_cv(img)
    img_8_mean = BitPlane_Slicing_Rebuild.getslicing_8_all(img_mean)  # 获取所有比特平面
    img_8_gaussian = BitPlane_Slicing_Rebuild.getslicing_8_all(img_gaussian)
    img_8_mean_change = BitPlane_Change.changeslicing_1(img_8_mean)  # 比特平面对调
    img_8_gaussian_change = BitPlane_Change.changeslicing_1(img_8_gaussian)
    img_8_mean_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_8_mean_change)  # 将比特平面重构为图像
    img_8_gaussian_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_8_gaussian_change)
    imgs = [img, img_mean, img_gaussian, img_rebuild, img_8_mean_rebuild, img_8_gaussian_rebuild]
    imgtitles = ["原图像", "5×5均值平滑后的图像", "5×5高斯平滑后的图像",
                 "比特平面直接对调", "均值平滑再对调后的图像", "高斯平滑再对调后的图像"]
    maintitle = ""
    show(imgs, imgtitles, maintitle, rows=2, cols=3)


def main_2():
    # img1 = cv.imread("../Picture/food1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img4 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    # check_2(img1)
    check_2(img2)
    check_2(img3)
    check_2(img4)


def check_3(img, num):
    # 对低比特进行平滑处理后
    # 加上高比特
    # 再对调
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)
    img_change = BitPlane_Change.changeslicing_1(img_8)
    img_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_change)
    img_re_low = LowBitPlane_Solve.rebuild_slicing_low_num(img_8, num)
    img_re_low_m, img_re_low_g = LowBitPlane_Solve.smooth_cv(img_re_low)
    img_add_m = LowBitPlane_Solve.add_high(img_re_low_m, num, img_8)
    img_add_g = LowBitPlane_Solve.add_high(img_re_low_m, num, img_8)
    img_m_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img_add_m)
    img_g_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img_add_g)
    img_m_8_change = BitPlane_Change.changeslicing_1(img_m_8)
    img_g_8_change = BitPlane_Change.changeslicing_1(img_g_8)
    img_m_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_m_8_change)
    img_g_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_g_8_change)
    imgs = [img, img_add_m, img_add_g, img_rebuild, img_m_rebuild, img_g_rebuild]
    imgtitles = ["原图像", "低比特均值平滑+高比特", "低比特高斯平滑+高比特",
                 "直接对调", "低比特均值+高比特+对调", "低比特高斯+高比特+对调"]
    maintitle = ""
    show(imgs, imgtitles, maintitle, rows=2, cols=3)


def main_3():
    num1 = 5
    # img1 = cv.imread("../Picture/feibiao1.png", cv.IMREAD_GRAYSCALE)
    num2 = 3
    img2 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    num3 = 4
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    num4 = 4
    img4 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    # check_3(img1, num1)
    check_3(img2, num2)
    check_3(img3, num3)
    check_3(img4, num4)


def check_4(img):
    # 进行伪彩色编码
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)  # 获取所有比特平面
    img_change = BitPlane_Change.changeslicing_1(img_8)  # 比特平面对调
    img_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_change)  # 将比特平面重构为图像
    Ts = GetThreshold.getTs(img_rebuild)
    print(Ts)
    img_r, img_g, img_b = GrayToColor.gray_to_3singal(img_rebuild, Ts)
    img_rgb = GrayToColor.grays_to_color(img_r, img_g, img_b)
    imgs = [img,  img_rebuild, img_rgb]
    imgtitle = ["原图像", "双边滤波处理后的图像", "均值滤波处理后的图像",
                "比特平面对换后的图像", "高斯滤波处理后的图像", "伪彩色增强后的图像"]


def main_4():
    return 0


def check_5(img):
    # 进行自适应伪彩色编码
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)  # 获取所有比特平面
    img_change = BitPlane_Change.changeslicing_1(img_8)  # 比特平面对调
    img_rebuild = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_change)  # 将比特平面重构为图像
    Ts = GetThreshold.getTs(img_rebuild)
    print(Ts)
    img_r, img_g, img_b = GrayToColor.gray_to_3singal_T(img_rebuild, Ts)
    img_rgb = GrayToColor.grays_to_color(img_r, img_g, img_b)
    imgs = [img, img_rebuild, img_rgb]
    imgtitles = ["原图像", "比特平面对调后的图像", "自适应彩虹码编码处理后的图像"]
    maintitle = ''
    show(imgs, imgtitles, maintitle, 1, 3)


def main_5():
    img1 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_5(img1)
    check_5(img2)
    check_5(img3)


if __name__ == "__main__":
    # 测试比特平面对调
    # main_1()
    # 对图像进行平滑处理后
    # 再进行比特平面对调
    # main_2()
    # 对低比特进行平滑处理后
    # 加上高比特
    # main_3()
    main_5()
