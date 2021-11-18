import numpy as np
import matplotlib.pyplot as plt
import EyeData as ed
from read_picture import readPicture


def plotLeftEye(ax1, lw, eye):
    XUp = np.linspace( eye.leftUpPoint/180 * np.pi, np.pi / 2, 200)
    XrightUp = np.linspace( np.pi /2, 0, 200)
    Xdown = np.linspace(3/2 * np.pi, eye.leftDownPoint / 180 * np.pi,  200)
    XrightDown = np.linspace(2 * np.pi, 3/2 * np.pi,  200)
    Xleft = np.linspace(eye.leftUpPoint/180 * np.pi, eye.leftDownPoint/180 * np.pi, 200)
    leftSide = [eye.leftL] * 200
    ax1.plot(XUp , eye.leftUpFun(XUp), linewidth = lw, color = 'red')
    ax1.plot(XrightUp , eye.leftRightFun(XrightUp), linewidth = lw, color = 'red')
    ax1.plot(Xdown, eye.leftDownFun(Xdown), linewidth = lw, color = 'red')
    ax1.plot(XrightDown, eye.leftDownRightFun(XrightDown), linewidth = lw, color = 'red')
    ax1.plot(Xleft, leftSide, linewidth = lw, color = 'red')
    plt.savefig('left.png')


def plotRightEye(ax1, lw, eye):
    Xup = np.linspace(eye.rightUpPoint/180 * np.pi, np.pi/2, 200)
    XleftUp = np.linspace( np.pi /2, np.pi, 200)
    Xdown = np.linspace( 3/2 * np.pi, (360 + eye.rightDownPoint)/180 * np.pi, 200)
    XleftDown = np.linspace(np.pi, 3/2 * np.pi,  200)
    
    rightSide = [eye.rightR] * 200
    Xright = np.linspace(eye.rightDownPoint/180 * np.pi, eye.rightUpPoint/180 * np.pi , 200)
    ax1.plot(Xup , eye.rightUpFun(Xup), linewidth = lw, color = 'green')
    ax1.plot(XleftUp , eye.rightLeftFun(XleftUp), linewidth = lw, color = 'green')
    ax1.plot(Xdown, eye.rightDownFun(Xdown), linewidth = lw, color = 'green')
    ax1.plot(XleftDown, eye.rightDownLeftFun(XleftDown), linewidth = lw, color = 'green')
    ax1.plot(Xright, rightSide, linewidth = lw, color = 'green')
    plt.savefig('right.png')


def plotBinocular(ax1, lw, eye):
    Xup = np.linspace(eye.leftUpPoint/180 * np.pi, eye.rightUpPoint / 180 * np.pi, 200)
    Xdown = np.linspace(eye.leftDownPoint / 180 * np.pi, (360 + eye.rightDownPoint)/180 * np.pi, 200)
    leftSide = [eye.leftL] * 200
    rightSide = [eye.rightR] * 200
    Xleft = np.linspace(eye.leftUpPoint/180 * np.pi, eye.leftDownPoint/180 * np.pi, 200)
    Xright = np.linspace(eye.rightDownPoint/180 * np.pi, eye.rightUpPoint/180 * np.pi , 200)
    ax1.plot(Xup , eye.topLimitFun(Xup), linewidth = lw, color = 'blue')
    ax1.plot(Xdown, eye.botLimitFun(Xdown), linewidth = lw, color = 'blue')
    ax1.plot(Xright, rightSide, linewidth = lw, color = 'blue')
    ax1.plot(Xleft, leftSide, linewidth = lw, color = 'blue')
    plt.savefig('binocular.png')


def plotFOV(visual = 'binocular'):
    theta = readPicture(fname = 'ThetaImage_FishEyeLens.pf')
    fig = plt.figure(figsize=(10,8))
    lw = 4.0
    ax1 = fig.add_axes([0,0, 1, 1],polar=True)
    ax1.set_ylim(0,90)
    ax1.set_yticks(np.arange(0,90, 20))
    
    if visual == 'left' :
        eye = ed.Monocular(theta, 'left')
        plotLeftEye(ax1, lw, eye)
    elif visual == 'right':
        eye = ed.Monocular(theta, 'right')
        plotRightEye(ax1, lw, eye)
    else:
        eye = ed.Binocular(theta)
        plotBinocular(ax1, lw, eye)

    plt.show()
    
