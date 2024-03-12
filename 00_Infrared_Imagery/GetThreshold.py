import cv2 as cv
import BitPlane_Slicing_Rebuild
import HistEqualization
import BitPlane_Slicing_Rebuild


def get_totalnum(pixnumlist, Lmin, Lmax):
    # 获取指定区域像素范围的像素个数
    totalnum = 0
    for i in range(Lmin, Lmax + 1):
        totalnum = totalnum + pixnumlist[i]
    return totalnum


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
            rou_square = (p1 * (m1 - mk[Lmax]) * (m1 - mk[Lmax])
                          + p2 * (m2 - mk[Lmax]) * (m2 - mk[Lmax]))
        if rou_square > maxrou_square:
            maxrou_square = rou_square
            maxk = k
    return maxk


def getTs(img):
    pixnumlist = HistEqualization.getpixnumlist(img)
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


def check_getT_area(img):
    pixnumlist = HistEqualization.getpixnumlist(img)
    T = getT_area(pixnumlist, 0, 255)
    img_change = binarization(img, T)
    imgs = [img, img_change]
    imgtitles = ["原图像", "使用阈值进行分割后的二值图像"]
    maintitle = "计算的阈值T={}".format(T)
    BitPlane_Slicing_Rebuild.show_2pic(imgs, imgtitles, maintitle)


def main_getT_area():
    img1 = cv.imread("../Picture/cat1.jpg", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("../Picture/INFRARED.png", cv.IMREAD_GRAYSCALE)
    check_getT_area(img1)
    check_getT_area(img2)


if __name__ == "__main__":
    main_getT_area()
