import cv2 as cv

import BitPlane_Slicing_Rebuild


def changeslicing_1(img_8):
    # 高4层和低4层比特平面互换
    # 此函数使用第1层与第8层对换
    img_change = img_8.copy()
    for i in range(4):
        temp = img_change[i].copy()
        img_change[i] = img_change[7 - i].copy()
        img_change[7 - i] = temp.copy()
    return img_change


def changeslicing_2(img_8):
    # 此函数使用第1层与第5层对换
    img_change = img_8.copy()
    for i in range(4):
        temp = img_change[i].copy()
        img_change[i] = img_change[i + 4].copy()
        img_change[i + 4] = temp.copy()
    return img_change


def changeslicing3(img_8):
    # 由于只有第6平面和第7平面清晰
    # 对换策略?
    # 只兑换第6平面和第7平面
    img_change = img_8.copy()
    temp = img_change[6 - 1]
    img_change[6 - 1] = img_change[7 - 1]
    img_change[7 - 1] = temp
    return img_change


def set0_1(img_8):
    # 除了第6 第7平面 全部置0
    bit_zero = img_8[0].copy()
    width, height = bit_zero.shape
    for i in range(width):
        for j in range(height):
            bit_zero[i, j] = 0
    img_change = img_8.copy()
    for i in range(8):
        if i != 5 and i != 6:
            img_change[i] = bit_zero.copy()
    return img_change


def set0_2(img_8):
    # 第2 3 4 全部置0
    bit_zero = img_8[0].copy()
    width, height = bit_zero.shape
    for i in range(width):
        for j in range(height):
            bit_zero[i, j] = 0
    img_change = img_8.copy()
    for i in range(8):
        if i == 1 and i == 2 and i == 3:
            img_change[i] = bit_zero.copy()
    return img_change


def set0_3(img_8):
    # 第1 2 3 4 全部置0
    bit_zero = img_8[0].copy()
    width, height = bit_zero.shape
    for i in range(width):
        for j in range(height):
            bit_zero[i, j] = 0
    img_change = img_8.copy()
    for i in range(4):
        img_change[i] = bit_zero.copy()
    return img_change


def check_changeslicing_1(img):
    # 测试分层对换函数
    img_8 = BitPlane_Slicing_Rebuild.getslicing_8_all(img)
    img_8_change = changeslicing_1(img_8)
    img_change = BitPlane_Slicing_Rebuild.rebuild_slicing_8(img_8_change)
    imgs = [img, img_change]
    imgtitles = ["原图像", "比特平面对调后的图像"]
    maintitle = "比特平面对调"
    BitPlane_Slicing_Rebuild.show_2pic(imgs, imgtitles, maintitle)


def main_changeslicing_1():
    # 放在main中执行
    img1 = cv.imread("../Picture/dark_cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/lingxiaohua.jpg", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("../Picture/Data-04-logo1b.jpg", cv.IMREAD_GRAYSCALE)
    img4 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_changeslicing_1(img1)
    check_changeslicing_1(img2)
    check_changeslicing_1(img3)
    check_changeslicing_1(img4)


if __name__ == "__main__":
    main_changeslicing_1()
