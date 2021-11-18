# Update: 10.11.2021
# Update for the Purpose of a GUI in the Bachelor Thesis of Florent Kqiku
# The updates involve Code where it is needed to read Paths,
# so the right Path is used in various Systems like macOS, Windows, Linux etc.
# Updates are also made, so the Scripts can take the loaded and selected pictures of the List in the GUI
# Update-Author: Florent Kqiku


import tkinter as tk
import read_picture as rp
from tkinter import messagebox
import array
import numpy as np
import matplotlib.pyplot as plt
import EyeData as ed
import util
import os
from pathlib import Path


def startFOVScript(selectedPf, upsidedown):
    for filename in selectedPf:

        try:
            f = open(filename, "rb")

            f.seek(32)  # find the number of row
            line = f.readline()
            row = eval(line)

            f.seek(46)  # find the number of column
            line = f.readline()
            col = eval(line)

            totalNumberOfBytes = row * col * 4  # calculate the total size of the img in byte
            f.seek(-totalNumberOfBytes, 2)  # move from the end of file
            imageData = f.readlines()

            byteImageFlattened = bytearray()
            for line in imageData:
                byteImageFlattened.extend(line)
            floatsArray = array.array('f', byteImageFlattened)

            imageMatrix = (np.array(floatsArray)).reshape((row, col))
            f.close()
            # return imageMatrix, filename, upsidedown
        except Exception as err:
            print(Exception, err)
            pass

        # %%
        # Change path to the path where the Theta and Omage Data are stored
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        theta, _, _ = rp.readPicture(fname=Path("../RD-GUI/Leuchtdichte Bilder/ThetaImage_FishEyeLens.pf"))
        omega, _, _ = rp.readPicture(fname=Path("../RD-GUI/Leuchtdichte Bilder/OmegaImage_FishEyeLens.pf"))
        radiansTheta = theta / 180 * np.pi
        fname = filename.split("/")[-1][:-3]
        # %%
        if upsidedown == True:
            im = np.flipud(imageMatrix)
        origin = np.where(theta == 0.)
        origin_row = origin[0][0]
        origin = [origin[1][0], origin[0][0]]
        # %%
        # Create a Folder, where the selected picture is Located to store the Results
        os.chdir(os.path.dirname(os.path.abspath(filename)))
        folderToCreate = fname + " - FOV"
        util.mkdir(folderToCreate)
        os.chdir(folderToCreate)
        # %%

        fig = plt.figure(figsize=(10, 8))
        plt.imshow(imageMatrix, cmap=plt.cm.gray, vmin=0, vmax=255)
        plt.savefig('Original.png')
        print('The original photo saved as Original.png \n')
        # %%
        cos_theta = np.cos(radiansTheta)
        try:
            E_ori = np.multiply(np.multiply(imageMatrix, cos_theta), omega)
        except Exception as err:
            print(Exception, err)
            print("The matrix dimension are not the same")
            tk.messagebox.showwarning("Warning", "The Matrix shape given by the chosen Image is not right!\n"
                                                 "Please upload another picture, taken with the right Camera\n"
                                                 "Note: The GUI works with the 'LMK mobile advanced'"
                                                 " based on a CANON EOS 550D"
                                                 "with a 4.5 mm objective lens (circular fisheye lens) "
                                                 "with a coverage angle of 140°.")

        upperImg = np.zeros(imageMatrix.shape)
        lowerImg = np.zeros(imageMatrix.shape)
        upperImg[:origin_row] = imageMatrix[:origin_row]
        lowerImg[origin_row:] = imageMatrix[origin_row:]
        util.plotImg(upperImg, 'Original_pic_upper.png', True, origin)
        util.plotImg(lowerImg, 'Original_pic_lower.png', True, origin)

        E_upimg = np.sum(E_ori[:origin_row])
        E_lowimg = np.sum(E_ori[origin_row:])
        E_ori = np.sum(E_ori)
        print(
            'The upper part and lower part of the original picture saved as Original_pic_upper.png and '
            'Original_pic_lower.png \n')

        # %%
        print('-------------------------FOV from Beleuchtungstechnik--------------------------\n')
        b = ed.Binocular(theta)
        mask = b.binocularMask()
        upperMask = np.zeros(mask.shape)
        lowerMask = np.zeros(mask.shape)
        upperMask[:origin_row] = mask[:origin_row]
        lowerMask[origin_row:] = mask[origin_row:]
        visualImg = np.multiply(mask, imageMatrix)
        visualOmega = np.multiply(mask, omega)
        cos_theta = np.multiply(np.cos(radiansTheta), mask)
        E_mat = np.multiply(np.multiply(visualImg, cos_theta), visualOmega)

        upperVisualImg = np.multiply(upperMask, visualImg)
        lowerVisualImg = np.multiply(lowerMask, visualImg)

        os.chdir(os.path.dirname(os.path.abspath(filename)))
        os.chdir(folderToCreate)

        util.plotImg(visualImg, 'Beleuchtungstechnik_Binocular.png', True, origin)
        util.plotImg(upperVisualImg, 'Beleuchtungstechnik_Binocular_upper.png', True, origin)
        util.plotImg(lowerVisualImg, 'Beleuchtungstechnik_Binocular_lower.png', True, origin)

        E_up = np.sum(E_mat[:origin_row])
        E_down = np.sum(E_mat[origin_row:])
        E_sum = np.sum(E_mat)
        print('The binocular FOV picture saved as Beleuchtungstechnik_Binocular.png')
        # %%
        leftEye = ed.Monocular(theta, 'left')
        leftMask = leftEye.leftMask()
        visualImgL = np.multiply(leftMask, imageMatrix)

        upperMaskL = np.zeros(leftMask.shape)
        lowerMaskL = np.zeros(leftMask.shape)
        upperMaskL[:origin_row] = leftMask[:origin_row]
        lowerMaskL[origin_row:] = leftMask[origin_row:]

        visualOmegaL = np.multiply(leftMask, omega)
        cos_thetaL = np.multiply(np.cos(radiansTheta), leftMask)
        E_left = np.multiply(np.multiply(visualImgL, cos_thetaL), visualOmegaL)

        upperVisualImgL = np.multiply(upperMaskL, visualImgL)
        lowerVisualImgL = np.multiply(lowerMaskL, visualImgL)

        os.chdir(os.path.dirname(os.path.abspath(filename)))
        os.chdir(folderToCreate)

        util.plotImg(visualImgL, 'Beleuchtungstechnik_LeftEye.png', True, origin)
        util.plotImg(upperVisualImgL, 'Beleuchtungstechnik_LeftEye_upper.png', True, origin)
        util.plotImg(lowerVisualImgL, 'Beleuchtungstechnik_LeftEye_lower.png', True, origin)

        E_leftup = np.sum(E_left[:origin_row])
        E_leftdown = np.sum(E_left[origin_row:])
        E_leftsum = np.sum(E_left)
        print('The left eye FOV picture saved as Beleuchtungstechnik_LeftEye.png')
        # %%

        rightEye = ed.Monocular(theta, 'right')
        rightMask = rightEye.rightMask()
        visualImgR = np.multiply(rightMask, imageMatrix)

        upperMaskR = np.zeros(rightMask.shape)
        lowerMaskR = np.zeros(rightMask.shape)
        upperMaskR[:origin_row] = rightMask[:origin_row]
        lowerMaskR[origin_row:] = rightMask[origin_row:]

        visualOmegaR = np.multiply(rightMask, omega)
        cos_thetaR = np.multiply(np.cos(radiansTheta), rightMask)
        E_right = np.multiply(np.multiply(visualImgR, cos_thetaR), visualOmegaR)

        upperVisualImgR = np.multiply(upperMaskR, visualImgR)
        lowerVisualImgR = np.multiply(lowerMaskR, visualImgR)

        os.chdir(os.path.dirname(os.path.abspath(filename)))
        os.chdir(folderToCreate)

        util.plotImg(visualImgR, 'Beleuchtungstechnik_RightEye.png', True, origin)
        util.plotImg(upperVisualImgR, 'Beleuchtungstechnik_RightEye_upper.png', True, origin)
        util.plotImg(lowerVisualImgR, 'Beleuchtungstechnik_RightEye_lower.png', True, origin)

        E_rightup = np.sum(E_right[:origin_row])
        E_rightdown = np.sum(E_right[origin_row:])
        E_rightsum = np.sum(E_right)
        print('The right eye FOV picture saved as Beleuchtungstechnik_RightEye.png\n')
        # %%
        print('-------------------------FOV from CIE Standard--------------------------\n')

        cie = ed.FOV_CIE_2(theta)
        CIEMask = cie.CIEMask()
        visualImgCIE = np.multiply(CIEMask, imageMatrix)
        visualOmegaCIE = np.multiply(CIEMask, omega)
        cos_thetaCIE = np.multiply(np.cos(radiansTheta), CIEMask)
        E_CIE = np.multiply(np.multiply(visualImgCIE, cos_thetaCIE), visualOmegaCIE)

        upperMaskCIE = np.zeros(CIEMask.shape)
        lowerMaskCIE = np.zeros(CIEMask.shape)
        upperMaskCIE[:origin_row] = CIEMask[:origin_row]
        lowerMaskCIE[origin_row:] = CIEMask[origin_row:]

        upperVisualImgCIE = np.multiply(upperMaskCIE, visualImgCIE)
        lowerVisualImgCIE = np.multiply(lowerMaskCIE, visualImgCIE)

        E_CIEup = np.sum(E_CIE[:origin_row])
        E_CIEdown = np.sum(E_CIE[origin_row:])
        E_CIEsum = np.sum(E_CIE)

        os.chdir(os.path.dirname(os.path.abspath(filename)))
        os.chdir(folderToCreate)

        util.plotImg(visualImgCIE, 'CIE.png', True, origin)
        util.plotImg(upperVisualImgCIE, 'CIE_upper.png', True, origin)
        util.plotImg(lowerVisualImgCIE, 'CIE_lower.png', True, origin)

        print('The binocular FOV picture saved as CIE.png\n')

        # %%

        fresult = open("result.txt", "w+")
        fresult.write("Illuminance of the original picture : {:.6} lx \n".format(E_ori))
        fresult.write(
            "                            upper part : {:.6} lx,  {:.6} % \n".format(E_upimg,
                                                                                    100 * E_upimg / E_ori))
        fresult.write(
            "                            lower part : {:.6} lx,  {:.6} % \n".format(E_lowimg,
                                                                                    100 * E_lowimg / E_ori))
        fresult.write("\n")

        fresult.write("With the definition from Beleuchtungstechnik: \n")
        fresult.write("Illuminance of the whole binocular FOV : {:.6} lx \n".format(E_sum))
        fresult.write(
            "                            upper part : {:.6} lx,  {:.6} % \n".format(E_up, 100 * E_up / E_sum))
        fresult.write(
            "                            lower part : {:.6} lx,  {:.6} % \n".format(E_down,
                                                                                    100 * E_down / E_sum))
        fresult.write("\n")
        fresult.write("Illuminance of the left eye FOV: {:.6} lx \n".format(E_leftsum))
        fresult.write("                         upper part : {:.6} lx,  {:.6} % \n".format(E_leftup,
                                                                                           100 * E_leftup /
                                                                                           E_leftsum))
        fresult.write("                         lower part : {:.6} lx,  {:.6} % \n".format(E_leftdown,
                                                                                           100 * E_leftdown /
                                                                                           E_leftsum))
        fresult.write("\n")
        fresult.write("Illuminance of the right eye FOV: {:.6} lx \n".format(E_rightsum))
        fresult.write("                            upper part : {:.6} lx,  {:.6} % \n".format(E_rightup,
                                                                                              100 * E_rightup /
                                                                                              E_rightsum))
        fresult.write("                            lower part : {:.6} lx,  {:.6} % \n".format(E_rightdown,
                                                                                              100 * E_rightdown
                                                                                              / E_rightsum))
        fresult.write("\n")
        fresult.write("\n")
        fresult.write("With the definition from CIE Standard: \n")
        fresult.write("Illuminance of the binocular FOV: {:.6} lx \n".format(E_CIEsum))
        fresult.write(
            "                            upper part : {:.6} lx,  {:.6} % \n".format(E_CIEup,
                                                                                    100 * E_CIEup / E_CIEsum))
        fresult.write("                            lower part : {:.6} lx,  {:.6} % \n".format(E_CIEdown,
                                                                                              100 * E_CIEdown /
                                                                                              E_CIEsum))
        fresult.write("                                                                      "
                      "                                         ")
        fresult.close()
        print('The results of are saved in result.txt \n')