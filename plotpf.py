import numpy as np
import array
import matplotlib.pyplot as plt


def plotimg(im, x, y):
    fig = plt.figure(figsize=(10,8))
    
    plt.imshow(im, cmap=plt.cm.gray, vmin = 0, vmax = 255)
    plt.scatter(x, y, c='r', s=40)
    plt.scatter(1184, 1014, c='r', s=40)
    plt.show()