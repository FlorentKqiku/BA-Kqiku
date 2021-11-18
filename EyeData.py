# Update: 10.11.2021
# Update for the Purpose of a GUI in the Bachelor Thesis of Florent Kqiku
# The only updates made, are in Row 19, 20 so the right Path is used in various Systems like macOS, Windows, Linux etc.
# Update-Author: Florent Kqiku


import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import util
import os
from pathlib import Path


class FOV_Beleuchtungstechink:
    
    def __init__(self, theta):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.up = pd.read_csv(Path('../RD-GUI/Gesichtsfeld/left_up.csv'), header = None)
        self.down = pd.read_csv(Path('../RD-GUI/Gesichtsfeld/left_down.csv'), header = None)
        self.leftUpPoint = self.up[1].iloc[0]
        self.leftDownPoint = self.down[1].iloc[-1]
        self.rightUpPoint = 180 - self.up[1].iloc[0]
        self.rightDownPoint = 180 - self.down[1].iloc[-1]
        self.leftL = 90.0
        self.rightR = 90.0
        self.theta = theta
        self.origin = np.ndarray.flatten(np.array(np.where(theta == 0.)))


class Monocular(FOV_Beleuchtungstechink):
    
    def __init__(self, theta, side):
        super().__init__(theta)
        if side == 'left':
            self.setLeftLimit()
        elif side == 'right':
            self.setRightLimit()
        else:
            print('error')
        
    def setLeftLimit(self):

        topIndex = np.where(self.up[1] == 90)[0][0]
        leftUp_r = self.up[0][0: topIndex + 1]
        leftUpRight_r = self.up[0][topIndex:]
        leftUp_rho = self.up[1][0: topIndex + 1] / 180 * np.pi
        leftUpRight_rho = self.up[1][topIndex:] / 180 * np.pi
        self.leftUpFun = interp1d(leftUp_rho, leftUp_r, kind = 'quadratic',fill_value='extrapolate')
        self.leftRightFun = interp1d(leftUpRight_rho, leftUpRight_r, kind = 'quadratic',fill_value='extrapolate')
        
        botIndex = np.where(self.down[1] == 270)[0][0]
        leftDown_r = self.down[0][botIndex : ]
        leftDown_rho = self.down[1][botIndex :] / 180 * np.pi
        leftDownRight_r = self.down[0][ : botIndex + 1]
        leftDownRight_rho = self.down[1][: botIndex + 1] / 180 * np.pi
        
        self.leftDownFun = interp1d(leftDown_rho, leftDown_r, kind = 'quadratic',fill_value='extrapolate')
        self.leftDownRightFun = interp1d(leftDownRight_rho, leftDownRight_r, kind = 'quadratic',fill_value='extrapolate')

        self.leftR = self.up[0].iloc[-1]
        row = self.theta[self.origin[0]]
        leftLIndex = np.argmin(np.abs(row - self.leftL))
        self.leftLIndex = np.array([self.origin[0], leftLIndex])
        # row = row[::-1]
        leftRIndex = row.shape[0] - 1 - np.argmin(np.abs(np.flipud(row) - self.leftR))

        self.leftRIndex = np.array([self.origin[0], leftRIndex])

    def setRightLimit(self):
        
        topIndex = np.where(self.up[1] == 90)[0][0]

        rightUp_r = self.up[0][0: topIndex + 1]
        rightUpLeft_r = self.up[0][topIndex:]

        rightUp_rho = np.pi- self.up[1][0: topIndex + 1] / 180 * np.pi
        rightUpLeft_rho = np.pi - self.up[1][topIndex:] / 180 * np.pi

        self.rightUpFun = interp1d(rightUp_rho, rightUp_r, kind = 'quadratic',fill_value='extrapolate')
        self.rightLeftFun= interp1d(rightUpLeft_rho, rightUpLeft_r, kind = 'quadratic',fill_value='extrapolate')
        # fup = interp1d(rho_rightup, r_rightup, kind = 'quadratic',fill_value='extrapolate')
        
        botIndex = np.where(self.down[1] == 270)[0][0]
        rightDown_r = self.down[0][botIndex : ]
        rightDown_rho = 3 * np.pi -self.down[1][botIndex :] / 180 * np.pi
        rightDownLeft_r = self.down[0][ : botIndex + 1]
        rightDownLeft_rho = 3 * np.pi-  self.down[1][: botIndex + 1] / 180 * np.pi
        
        
        self.rightDownFun = interp1d(rightDown_rho, rightDown_r, kind = 'quadratic',fill_value='extrapolate')
        self.rightDownLeftFun = interp1d(rightDownLeft_rho, rightDownLeft_r, kind = 'quadratic',fill_value='extrapolate')
        # rho_leftdown = self.down[1] / 180 * np.pi
        # r_leftdown = self.down[0]
        # rho_rightdown = 3 * np.pi - rho_leftdown
        # r_rightdown = r_leftdown
        # fdown = interp1d(rho_rightdown, r_rightdown, kind = 'quadratic',fill_value='extrapolate')

        # self.rightUpFun = fup
        # self.rightDownFun = fdown
        self.rightL = self.up[0].iloc[-1]

        row = self.theta[self.origin[0]]
        rightLIndex = np.argmin(np.abs(row - self.rightL))
        self.rightLIndex = np.array([self.origin[0], rightLIndex])
        # row = row[::-1]
        rightRIndex = row.shape[0] - 1 - np.argmin(np.abs(np.flipud(row) - self.rightR))
        self.rightRIndex = np.array([self.origin[0], rightRIndex])

    def verticesLImage(self):
        # LeftIndox = c1,
        rho_left, _ = util.cart2pol((self.leftLIndex - self.origin)[1], (self.leftLIndex - self.origin)[0])

        leftUp_X, leftUp_Y = util.pol2cart(rho_left, self.leftUpPoint / 180 * np.pi)
        leftUp_col = round(self.origin[1] + leftUp_X)
        leftDown_X, leftDown_Y = util.pol2cart(rho_left, self.leftDownPoint / 180 * np.pi)
        leftDown_col = round(self.origin[1] + leftDown_X)
        
        nXLeftUp = int(self.origin[1] - leftUp_col)
        nXRightUp = int(self.leftRIndex[1] - self.origin[1])
        
        nXLeftDown = int(self.origin[1] -  leftDown_col)
        nXLeftRightDown = int(self.leftRIndex[1] - self.origin[1])
        
        self.XLeftUp = np.linspace(self.leftUpPoint / 180 * np.pi, np.pi / 2, nXLeftUp)
        self.XLeftRightUp = np.linspace(np.pi / 2, 0, nXRightUp)
        self.XLeftDown = np.linspace(3/2 * np.pi, self.leftDownPoint / 180 * np.pi, nXLeftDown)
        self.XLeftRightDown = np.linspace(2 * np.pi, 3/2 * np.pi, nXLeftRightDown)
        return int(leftUp_col), int(leftDown_col)

    def verticesRImage(self):
        rho_right, _ = util.cart2pol((self.rightRIndex - self.origin)[1], (self.rightRIndex - self.origin)[0])

        rightUp_X, rightUp_Y = util.pol2cart(rho_right, self.rightUpPoint / 180 * np.pi)
        rightUp_col = round(self.origin[1] + rightUp_X)
        
        rightDown_X, rightDown_Y = util.pol2cart(rho_right, self.rightDownPoint / 180 * np.pi)
        rightDown_col = round(self.origin[1] + rightDown_X)
        
        nXRightUp = int(rightUp_col - self.origin[1])
        nXRightLeftUp = int(self.origin[1] - self.rightLIndex[1])

        nXRightDown = int(rightDown_col - self.origin[1])
        nXRightLeftDown = int(self.origin[1] - self.rightLIndex[1])
        
        self.XRightUp = np.linspace(self.rightUpPoint / 180 * np.pi, np.pi / 2, nXRightUp)
        self.XRightLeftUp = np.linspace(np.pi / 2, np.pi, nXRightLeftUp)

        
        self.XRightDown = np.linspace(3/2 * np.pi, (self.rightDownPoint +360) / 180 * np.pi, nXRightDown)
        self.XRightLeftDown = np.linspace( np.pi, 3/2 * np.pi, nXRightLeftDown)
        return int(rightUp_col), int(rightDown_col)
    
    def getImgLIndex(self):
        leftUp, leftDown = self.verticesLImage()
        topUpX = self.leftUpFun(self.XLeftUp)
        topRightX = self.leftRightFun(self.XLeftRightUp)

        botDownX = self.leftDownFun(self.XLeftDown)
        botRightX = self.leftDownRightFun(self.XLeftRightDown)
        botDownX = botDownX[::-1]
        botRightX = botRightX[::-1]

        upLeftRow, upLeftCol = util.findNearestValue(self.theta, topUpX , leftUp, self.origin[1])
        upLeftRightRow, upLeftRightCol = util.findNearestValue(self.theta, topRightX , self.origin[1], self.leftRIndex[1])
        
        downLeftRow, downLeftCol =  util.findNearestValue(np.flipud(self.theta), botDownX , leftDown, self.origin[1])
        downLeftRightRow, downLeftRightCol = util.findNearestValue(np.flipud(self.theta), botRightX , self.origin[1], self.leftRIndex[1])
        downLeftRow = self.theta.shape[0] - downLeftRow
        downLeftRightRow = self.theta.shape[0] - downLeftRightRow
        
        nLeftUp = leftUp - self.leftLIndex[1]
        leftUpX = [self.leftL] * nLeftUp
        upLeftSideRow, upLeftSideCol = util.findNearestValue(self.theta, leftUpX , self.leftLIndex[1], leftUp)
        
        nLeftDown = leftDown - self.leftLIndex[1]
        leftDownX = [self.leftL] * nLeftDown
        downLeftSideRow, downLeftSideCol = util.findNearestValue(np.flipud(self.theta), leftDownX , self.leftLIndex[1], leftDown)
        downLeftSideRow = self.theta.shape[0] - downLeftSideRow
        
        topCurve = [np.concatenate((upLeftSideCol, upLeftCol, upLeftRightCol)), np.concatenate((upLeftSideRow, upLeftRow, upLeftRightRow))]
        botCurve = [np.concatenate((downLeftSideCol, downLeftCol, downLeftRightCol)), np.concatenate((downLeftSideRow, downLeftRow, downLeftRightRow))]
        return topCurve, botCurve
    
    def getImgRIndex(self):
        rightUp, rightDown = self.verticesRImage()
        topUpX = self.rightUpFun(self.XRightUp)
        topLeftX = self.rightLeftFun(self.XRightLeftUp)

        botDownX = self.rightDownFun(self.XRightDown)
        botLeftX = self.rightDownLeftFun(self.XRightLeftDown)
        # print(botDownX)

        upRightRow, upRightCol = util.findNearestValue(self.theta, np.flipud(topUpX) , self.origin[1], rightUp)
        # upRightCol = self.theta.shape[1] - upRightCol - 1
        upRightLeftRow, upRightLeftCol = util.findNearestValue(self.theta, np.flipud(topLeftX) , self.rightLIndex[1], self.origin[1])
        
        downRightRow, downRightCol =  util.findNearestValue(np.flipud(self.theta), botDownX , self.origin[1], rightDown)
        downRightLeftRow, downRightLeftCol = util.findNearestValue(np.flipud(self.theta), botLeftX , self.rightLIndex[1], self.origin[1])
        
        downRightRow = self.theta.shape[0] - downRightRow - 1
        downRightLeftRow = self.theta.shape[0] - downRightLeftRow - 1

        
        nRightUp = self.rightRIndex[1] -  rightUp
        rightUpX = [self.rightR] * nRightUp
        upRightSideRow, upRightSideCol = util.findNearestValue(self.theta, rightUpX , rightUp, self.rightRIndex[1])
        
        nRightDown = self.rightRIndex[1] - rightDown
        rightDownX = [self.rightR] * nRightDown
        downRightSideRow, downRightSideCol = util.findNearestValue(np.flipud(self.theta), rightDownX , rightDown, self.rightRIndex[1])
        downRightSideRow = self.theta.shape[0] - downRightSideRow
        
        topCurve = [np.concatenate((  upRightLeftCol, upRightCol, upRightSideCol)), np.concatenate(( upRightLeftRow, upRightRow, upRightSideRow,))]
        botCurve = [np.concatenate(( downRightLeftCol, downRightCol, downRightSideCol)), np.concatenate(( downRightLeftRow, downRightRow, downRightSideRow, ))]
        return topCurve, botCurve
    
    def rightMask(self):
        topCurve, botCurve = self.getImgRIndex()
        mask = np.zeros(self.theta.shape)
        for i in range(0, topCurve[0].shape[0]):
            for j in range(topCurve[1][i], botCurve[1][i]):
                mask[j][topCurve[0][i]] = 1
        return mask
    
    def leftMask(self):
        topCurve, botCurve = self.getImgLIndex()
        mask = np.zeros(self.theta.shape)
        for i in range(0, topCurve[0].shape[0]):
            for j in range(topCurve[1][i], botCurve[1][i]):
                mask[j][topCurve[0][i]] = 1
        return mask


class Binocular(FOV_Beleuchtungstechink):
    
    def __init__(self, theta):
        super().__init__(theta)
        self.setTopLimit()
        self.setBotLimit()
        row = self.theta[self.origin[0]]
        leftIndex = np.argmin(np.abs(row - self.leftL))
        self.leftIndex = np.array([self.origin[0], leftIndex])
        row = row[::-1]
        rightIndex = row.shape[0] - 1 - np.argmin(np.abs(row - self.rightR))
        self.rightIndex = np.array([self.origin[0], rightIndex])
        
    def setTopLimit(self):
        topIndex = np.where(self.up[1] == 90)[0][0]
        topVertex = self.up[0][topIndex]
        leftUp = self.up[0][0: topIndex + 1]
        rightUp = self.up[0][0: topIndex][::-1]
        leftX = self.up[1][0: topIndex + 1]
        rightX = 180 - self.up[1][0: topIndex][::-1]
        upLimit = np.concatenate((leftUp, rightUp))
        upX = np.concatenate((leftX, rightX))
        fup = interp1d(upX / 180 * np.pi, upLimit, kind = 'quadratic',fill_value='extrapolate')
        self.topLimitFun = fup
        self.topPoint = topVertex
        
    def setBotLimit(self):
        botIndex = np.where(self.down[1] == 270)[0][0]
        botVertex = self.down[0][botIndex]
        leftDown = self.down[0][botIndex::][::-1]
        rightDown = self.down[0][botIndex+1::]
        leftX = self.down[1][botIndex :: ][::-1]
        rightX = 540 - self.down[1][botIndex +1::]
        downLimit = np.concatenate((leftDown, rightDown))
        downX = np.concatenate((leftX, rightX))
        fdown = interp1d(downX / 180 * np.pi, downLimit, kind = 'quadratic',fill_value='extrapolate')
        self.botLimitFun = fdown
        self.botPoint = botVertex
    
    def verticesInImage(self):
        rho_right, _ = util.cart2pol((self.rightIndex - self.origin)[1], (self.rightIndex - self.origin)[0])
        rho_left, _ = util.cart2pol((self.leftIndex - self.origin)[1], (self.leftIndex - self.origin)[0])
        leftUp_X, leftUp_Y = util.pol2cart(rho_left, self.leftUpPoint / 180 * np.pi)
        leftUp_col = round(self.origin[1] + leftUp_X)

        leftDown_X, leftDown_Y = util.pol2cart(rho_left, self.leftDownPoint / 180 * np.pi)
        leftDown_col = round(self.origin[1] + leftDown_X)
        
        rightUp_X, rightUp_Y = util.pol2cart(rho_right, self.rightUpPoint / 180 * np.pi)
        rightUp_col = round(rightUp_X + self.origin[1])
        
        rightDown_X, rightDown_Y = util.pol2cart(rho_right, self.rightDownPoint / 180 * np.pi)
        rightDown_col = round(rightDown_X + self.origin[1])

        nXup = int(rightUp_col - leftUp_col)
        nXdown = int(rightDown_col - leftDown_col)

        self.Xup = np.linspace(self.leftUpPoint / 180 * np.pi, self.rightUpPoint / 180 * np.pi, nXup)
        
        self.Xdown = np.linspace(self.leftDownPoint / 180 * np.pi, (360 + self.rightDownPoint) / 180 * np.pi, nXdown)
        return int(leftUp_col), int(rightUp_col), int(leftDown_col), int(rightDown_col)
    
    def getImgIndex(self):
        leftUp, rightUp, leftDown, rightDown = self.verticesInImage()
        topX = self.topLimitFun(self.Xup)
        botX = self.botLimitFun(self.Xdown)
        upRowInd, upColInd = util.findNearestValue(self.theta, topX , leftUp, rightUp)
        downRowInd, downColInd = util.findNearestValue(np.flipud(self.theta), botX , leftDown, rightDown)
        downRowInd = self.theta.shape[0] - downRowInd
        
        nLeftUp = leftUp - self.leftIndex[1]
        leftUpX = [self.leftL] * nLeftUp
        upLeftSideRow, upLeftSideCol = util.findNearestValue(self.theta, leftUpX , self.leftIndex[1], leftUp)
        
        nRightUp = self.rightIndex[1] - rightUp
        rightUpX = [self.rightR] * (nRightUp + 1)
        upRightSideRow, upRightSideCol = util.findNearestValue(self.theta, rightUpX, rightUp, self.rightIndex[1] + 1)
        
        nLeftDown = leftDown - self.leftIndex[1]
        leftDownX = [self.leftL] * nLeftDown
        downLeftSideRow, downLeftSideCol = util.findNearestValue(np.flipud(self.theta), leftDownX , self.leftIndex[1], leftDown)
        downLeftSideRow = self.theta.shape[0] - downLeftSideRow
        
        nRightDown =  self.rightIndex[1] - rightDown
        rightDownX = [self.rightR] * (nRightDown + 1)
        downRightSideRow, downRightSideCol = util.findNearestValue(np.flipud(self.theta), rightDownX , rightDown, self.rightIndex[1] + 1)
        downRightSideRow = self.theta.shape[0] - downRightSideRow

        topCurve = [np.concatenate((upLeftSideCol, upColInd, upRightSideCol)), np.concatenate((upLeftSideRow, upRowInd, upRightSideRow))]
        botCurve = [np.concatenate((downLeftSideCol, downColInd, downRightSideCol)), np.concatenate((downLeftSideRow, downRowInd, downRightSideRow))]
        return topCurve, botCurve
    
    def binocularMask(self):
        topCurve, botCurve = self.getImgIndex()
        
        mask = np.zeros(self.theta.shape)
        for i in range(0, topCurve[0].shape[0]):
            for j in range(topCurve[1][i], botCurve[1][i]):
                mask[j][topCurve[0][i]] = 1
        return mask


class FOV_CIE:
    
    def __init__(self, theta):
        self.upperLimit = 50
        self.lowerLimit = 70
        self.theta = theta
        self.origin = np.ndarray.flatten(np.array(np.where(theta == 0.)))
        
    def findIndex(self):
        upperArea = self.theta[0 : self.origin[0] + 1]
        lowerArea = self.theta[self.origin[0] ::]
        upperIndices = []
        lowerIndices = []

        for j in range(upperArea.shape[1]):
            i_up = np.argmin(np.abs((upperArea.T)[j] - 50))
            i_down = np.argmin(np.abs((lowerArea.T)[j] - 70)) + self.origin[0]
            if i_down > self.origin[0]:
                lowerIndices.append([i_down, j])
            if i_up < upperArea.shape[0] -1:
                upperIndices.append([i_up,j])
        
        return np.array(upperIndices), np.array(lowerIndices)
    
    def mask(self):
        upperIndices, lowerIndices = self.findIndex()
        leftDownCol = lowerIndices[0][1]
        leftUpCol = upperIndices[0][1]
        rightUpCol = upperIndices[-1][1]
        rightDownCol = lowerIndices[-1][1]
        leftSide = []
        rightSide =[]
        for i in range(leftDownCol, leftUpCol):
            leftSide.append([self.origin[0], i])
        for i in range(rightUpCol + 1, rightDownCol + 1):
            rightSide.append([self.origin[0], i])
        
        upperIndices = np.concatenate((np.array(leftSide), upperIndices))
        upperIndices = np.concatenate((upperIndices, np.array(rightSide)))
        mask = np.zeros(self.theta.shape)
        for j, col in enumerate(upperIndices):
            for i in range(upperIndices[j][0], lowerIndices[j][0]):
                mask[i][upperIndices[j][1]] = 1
        return mask


class FOV_CIE_2:
    def __init__(self, theta):
        self.theta = theta
        self.origin = np.ndarray.flatten(np.array(np.where(theta == 0.)))
        self.leftUpPoint = np.array([146.2510, 90.0])
        self.upPoint = np.array([90.0, 50.0])
        self.rightUpPoint = np.array([33.7490, 90.0])
        
        self.leftDownPoint = np.array([231.0576, 90.0])
        self.downPoint = np.array([270.0, 70.0])
        self.rightDownPoint = np.array([308.9424, 90.0])
        
        row = self.theta[self.origin[0]]
        leftIndex = np.argmin(np.abs(row - 90.0))
        self.leftIndex = np.array([self.origin[0], leftIndex])
        row = row[::-1]
        rightIndex = row.shape[0] - 1 - np.argmin(np.abs(row - 90.0))
        self.rightIndex = np.array([self.origin[0], rightIndex])
        self.setTopLimit()
        self.setBotLimit()
        
    def setTopLimit(self):

        phi = np.array([146.2510, 90.0, 33.7490])
        theta = np.array([90.0, 50.0, 90.0])
        
        fup = interp1d(phi / 180 * np.pi, theta, kind = 'quadratic',fill_value='extrapolate')
        self.topFun = fup
    
    def setBotLimit(self):
        phi = np.array([231.0576, 270.0, 308.9424])
        theta = np.array([90.0, 70.0, 90.0])
        
        fdown = interp1d(phi / 180 * np.pi, theta, kind = 'quadratic',fill_value='extrapolate')
        self.botFun = fdown

    def verticesInImage(self):
        rho_right, _ = util.cart2pol((self.rightIndex - self.origin)[1], (self.rightIndex - self.origin)[0])
        rho_left, _ = util.cart2pol((self.leftIndex - self.origin)[1], (self.leftIndex - self.origin)[0])
        leftUp_X, leftUp_Y = util.pol2cart(rho_left, self.leftUpPoint[0] / 180 * np.pi)
        leftUp_col = round(self.origin[1] + leftUp_X)

        leftDown_X, leftDown_Y = util.pol2cart(rho_left, self.leftDownPoint[0] / 180 * np.pi)
        leftDown_col = round(self.origin[1] + leftDown_X)
        
        rightUp_X, rightUp_Y = util.pol2cart(rho_right, self.rightUpPoint[0] / 180 * np.pi)
        rightUp_col = round(rightUp_X + self.origin[1])
        
        rightDown_X, rightDown_Y = util.pol2cart(rho_right, self.rightDownPoint[0] / 180 * np.pi)
        rightDown_col = round(rightDown_X + self.origin[1])

        nXup = int(rightUp_col - leftUp_col)
        nXdown = int(rightDown_col - leftDown_col)


        self.Xup = np.linspace(self.leftUpPoint[0] / 180 * np.pi, self.rightUpPoint[0] / 180 * np.pi, nXup)
        
        self.Xdown = np.linspace(self.leftDownPoint[0] / 180 * np.pi, self.rightDownPoint[0] / 180 * np.pi, nXdown)

        return int(leftUp_col), int(rightUp_col), int(leftDown_col), int(rightDown_col)
    
    def getImgIndex(self):
        leftUp, rightUp, leftDown, rightDown = self.verticesInImage()
        topX = self.topFun(self.Xup)
        botX = self.botFun(self.Xdown)
        upRowInd, upColInd = util.findNearestValue(self.theta, topX , leftUp, rightUp)
        downRowInd, downColInd = util.findNearestValue(np.flipud(self.theta), botX , leftDown, rightDown)
        downRowInd = self.theta.shape[0] - downRowInd
        
        nLeftUp = leftUp - self.leftIndex[1]
        leftUpX = [90.0] * nLeftUp
        upLeftSideRow, upLeftSideCol = util.findNearestValue(self.theta, leftUpX , self.leftIndex[1], leftUp)
        
        nRightUp = self.rightIndex[1] - rightUp
        rightUpX = [90.0] * (nRightUp + 1)
        upRightSideRow, upRightSideCol = util.findNearestValue(self.theta, rightUpX, rightUp, self.rightIndex[1] + 1)
        
        nLeftDown = leftDown - self.leftIndex[1]
        leftDownX = [90.0] * nLeftDown
        downLeftSideRow, downLeftSideCol = util.findNearestValue(np.flipud(self.theta), leftDownX , self.leftIndex[1], leftDown)
        downLeftSideRow = self.theta.shape[0] - downLeftSideRow
        
        nRightDown =  self.rightIndex[1] - rightDown
        rightDownX = [90.0] * (nRightDown + 1)
        downRightSideRow, downRightSideCol = util.findNearestValue(np.flipud(self.theta), rightDownX , rightDown, self.rightIndex[1] + 1)
        downRightSideRow = self.theta.shape[0] - downRightSideRow

        topCurve = [np.concatenate((upLeftSideCol, upColInd, upRightSideCol)), np.concatenate((upLeftSideRow, upRowInd, upRightSideRow))]
        botCurve = [np.concatenate((downLeftSideCol, downColInd, downRightSideCol)), np.concatenate((downLeftSideRow, downRowInd, downRightSideRow))]
        return topCurve, botCurve

    def CIEMask(self):
        topCurve, botCurve = self.getImgIndex()
        
        mask = np.zeros(self.theta.shape)
        for i in range(0, topCurve[0].shape[0]):
            for j in range(topCurve[1][i], botCurve[1][i]):
                mask[j][topCurve[0][i]] = 1
        return mask
        