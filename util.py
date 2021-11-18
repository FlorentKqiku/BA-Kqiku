import numpy as np
import matplotlib.pyplot as plt
import os

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def plotImg(im, name, image = True, *argv):
    fig = plt.figure(figsize=(10,8))
    if image:
        plt.imshow(im, cmap=plt.cm.gray, vmin = 0, vmax = 255)
    else:
        plt.imshow(im, cmap=plt.cm.gray)
    for arg in argv:
        plt.scatter(arg[0], arg[1], c='red', s = 40)
    plt.savefig(name)

def plots(im, points):
    fig = plt.figure(figsize=(10,8))
    plt.imshow(im, cmap=plt.cm.gray)
    for p in points:
        plt.scatter(p[1], p[0], c='red', s = 10)

def findNearestValue(mat, arr, start, stop):
    rowArr = np.zeros(stop - start, dtype = int)
    for i in range(start, stop):
        rowArr[i - start] = np.argmin(np.abs(mat[:,i] - arr[i - start]))
    colArr = np.arange(start, stop)
    return rowArr, colArr
    
def mkdir(foldername):

    folder_dir = os.path.join(os.path.abspath(os.curdir), foldername)

    try:
        os.mkdir(folder_dir)
    except OSError:
        pass
    
