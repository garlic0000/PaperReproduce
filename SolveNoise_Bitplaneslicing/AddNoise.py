import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]


# 添加椒噪声
def add_pepper_noise(img, percentage):
    # percentage 为信噪比
    img_n = img.copy()
    # 信噪比
    height, width = img_n.shape
    noisenum = int((1 - percentage) * height * width)
    for i in range(noisenum):
        posw = np.random.randint(0, height - 1)
        posh = np.random.randint(0, width - 1)
        img_n[posw, posh] = 0
    return img_n


# 添加椒噪声
def add_salt_noise(img, percentage):
    # percentage 为信噪比
    img_n = img.copy()
    # 信噪比
    height, width = img_n.shape
    noisenum = int((1 - percentage) * height * width)
    for i in range(noisenum):
        posw = np.random.randint(0, height - 1)
        posh = np.random.randint(0, width - 1)
        img_n[posw, posh] = 255
    return img_n


# 添加椒盐噪声
def add_pepper_salt_noise(img, percentage):
    # percentage 为信噪比
    img_n = img.copy()
    # 信噪比
    height, width = img_n.shape
    noisenum = int((1 - percentage) * height * width)
    for i in range(noisenum):
        posw = np.random.randint(0, height - 1)
        posh = np.random.randint(0, width - 1)
        # 0 和 255 随机选择
        if np.random.randint(0, 1) == 0:
            img_n[posw, posh] = 0
        else:
            img_n[posw, posh] = 255
    return img_n


# https://blog.csdn.net/poisonchry/article/details/110847127
# 高斯噪声
def add_gaussian_noise():
    img = cv.imread("../Picture/cat1.jpg", cv.IMREAD_GRAYSCALE)
    percentage = 0.6


def show_img_noise(img, p):
    img_n = add_salt_noise(img, p)
    imgs = [img, img_n]
    imgtitle = ["原图像", "增加椒盐噪声的图像"]
    fig, axe = plt.subplots(nrows=1, ncols=2)
    for i in range(len(imgs)):
        axe[i].imshow(imgs[i], cmap='gray', vmin=0, vmax=255)
        axe[i].set_title(imgtitle[i], fontsize=10)
        axe[i].axis(False)
    plt.tight_layout()
    plt.show()


def main_noise():
    p = 0.98
    img = cv.imread("../Picture/cat1.jpg", cv.IMREAD_GRAYSCALE)
    show_img_noise(img, p)


if __name__ == "__main__":
    main_noise()
