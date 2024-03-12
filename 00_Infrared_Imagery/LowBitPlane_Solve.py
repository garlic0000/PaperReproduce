import numpy as np
import cv2 as cv
import BitPlane_Slicing_Rebuild


def mean_filter(img, m):
    # 均值滤波 m×m为滤波盒的尺寸
    # 填充0
    height, width = img.shape
    img_expand = np.zeros((height + 2 * (m // 2), width + 2 * (m // 2)))
    for i in range(m // 2, height + m // 2):
        for j in range(m // 2, width + m // 2):
            img_expand[i, j] = img[i - m // 2, j - m // 2]
    img_mean = img.copy()
    for i in range(m // 2, height + m // 2):
        for j in range(m // 2, width + m // 2):
            # 滤波盒均值运算
            sum_pix = 0
            for p in range(i - m // 2, i + m // 2):
                for q in range(j - m // 2, j + m // 2):
                    sum_pix = sum_pix + img_expand[p, q]
            ave_pix = sum_pix // (m * m)
            img_mean[i - m // 2, j - m // 2] = ave_pix
    return img_mean


def smooth_cv(img_noise):
    # 5×5均值滤波
    img_mean = cv.blur(img_noise, ksize=(5, 5))
    # 5×5高斯滤波
    img_gaussian = cv.GaussianBlur(img_noise, (5, 5), sigmaX=0, sigmaY=0)
    return img_mean, img_gaussian


def rebuild_slicing_low_num(img_8, num):
    # 只将低num个比特进行合成
    height, width = img_8[0].shape
    img_re_low_num = img_8[0].copy()
    for i in range(height):
        for j in range(width):
            pixnum = 0
            for n in range(num):
                pixnum = pixnum + img_8[n][i, j] * int(pow(2, n))
            img_re_low_num[i, j] = pixnum
    return img_re_low_num


def add_high(img_mean, num, img_8):
    # 将高比特平面上的值加入到进行去噪的低比特平面
    # num为低平面的个数
    height, width = img_mean.shape
    img_add = img_mean.copy()
    for i in range(height):
        for j in range(width):
            pixnum = img_mean[i, j]
            for n in range(num, 8):
                pixnum = pixnum + img_8[n][i, j] * int(pow(2, n))
            img_add[i, j] = pixnum
    return img_add


def check_meanfilter(img, m):
    imgm = mean_filter(img, m)
    imgs = [img, imgm]
    imgtitles = ["原图像", "使用{0}×{1}均值滤波器进行平滑".format(m, m)]
    maintitle = "均值滤波"
    BitPlane_Slicing_Rebuild.show_2pic(imgs, imgtitles, maintitle)


def main_meanfilter():
    m = 5
    img1 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/lingxiaohua.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    check_meanfilter(img2, m)


def check_lowbitsolve():
    img = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)
    img_re_low = rebuild_slicing_low_num(img_8, 4)
    img_re_low_m = mean_filter(img_re_low, 5)
    img_add = add_high(img_re_low_m, 4, img_8)
    imgs = [img, img_add]
    imgtitles = ["原图像", "低比特平滑处理后+高比特的图像"]
    maintitle = "低比特平滑处理再加上高比特"
    BitPlane_Slicing_Rebuild.show_2pic(imgs, imgtitles, maintitle)


if __name__ == "__main__":
    check_lowbitsolve()
