# Sets the GUI for the python program that calculates the RFOV for .pf pictures
# and creates Directograms for the selected .pf pictures.
#
# The Size is set, so it fits in every screen in normal Notebooks and external Screens.
# Once started you can choose as much pictures as you want and then select them individual from each other.
# After every calculation, you can start again without restarting the GUI
#
# Usage: Just run the "image_prozessing.py" file. and the GUI starts automatically.
#
# Author: Florent Kqiku
# Date: 10.11.2021


import subprocess
import tkinter as tk
import image_processing as ip
from tkinter import *
from tkinter import messagebox, filedialog
import sys
import os
import ntpath
from PIL import ImageTk, Image
import FOV_Script as fs


class Interface:
    def __init__(self, init_interface_window, imageProcessing):
        self.checkVar3 = tk.BooleanVar()
        self.checkVar2 = tk.IntVar()
        self.checkVar1 = tk.IntVar()
        self.init_interface = init_interface_window
        self.fname = ""
        self.imageProcessing = imageProcessing
        self.callFOV = IntVar()
        self.callDir = IntVar()
        self.FOVDone = IntVar()
        self.DirDone = IntVar()

    # The following function is based on the function from nguen, but changed for my Task
    # since i need to use his calculations
    def closeWindow(self):
        self.fname = None
        self.init_interface.destroy()
        sys.exit(0)

    # Activates the Continue Button (Calculate Button)
    def activateEvalButton(self):
        self.init_interface.continueButton.config(state=ACTIVE)

    # Set which data format can be opened with the Dialog Box
    def openFile(self):
        fileFormat = (("pf files", "*.pf"), ("All files", "*.*"))
        self.filenames = filedialog.askopenfilenames(title="Open File", initialdir="/", filetypes=fileFormat)
        self.init_interface.checkBtn1.config(state=ACTIVE)
        self.init_interface.checkBtn2.config(state=ACTIVE)
        self.writeListbox()

    # Returns the selected files from the Listbox
    def returnSelectedPictures(self):
        selectedPictures = []
        pictureIndex = self.init_interface.filenameListbox.curselection()
        for i in pictureIndex:
            pictureName = self.init_interface.filenameListbox.get(i)
            selectedPictures.append(pictureName)
        return selectedPictures

    # Write selected Files on Listbox
    def writeListbox(self):
        self.init_interface.filenameListbox.delete(0, tk.END)
        filenames = self.filenames
        if filenames == "":
            self.init_interface.filenameListbox.insert(0, "No file selected yet...")
        else:
            i = 1
            for singleFilenames in filenames:
                self.init_interface.filenameListbox.insert(i, singleFilenames)
                i = i + 1

    # The following function is based on the function from nguen, but changed for my Task
    # since i need to use his calculations
    def upsidedown(self):
        if self.checkVar3.get():
            self.upsidedown = True
        else:
            self.upsidedown = False

    # Set if need to create Directogram or FOV or even both
    def setWhichScriptToCall(self):
        if self.checkVar1.get() == 1 and self.checkVar2.get() == 1:
            self.callDir = 1
            self.callFOV = 1
        elif self.checkVar1.get() == 0 and self.checkVar2.get() == 1:
            self.callDir = 0
            self.callFOV = 1
        elif self.checkVar1.get() == 1 and self.checkVar2.get() == 0:
            self.callDir = 1
            self.callFOV = 0
        self.startDirectogramScript()
        self.startFOVScript()

    # Loop to show the .txt Result of the FOV and to which pictures the Results belong
    def resultFOVLoop(self):
        try:

            if self.FOVDone == 1:
                selectedPf = self.returnSelectedPictures()
                for filename in selectedPf:
                    with open("result.txt", "r") as r:
                        self.init_interface.resultLabelFOV.config(text=r.read())
                    # Get just the name of the File, without the path
                    file = ntpath.basename(filename)
                    result = "Results for FOV: " + file + "\n\nNote: To look up the other results and the Restricted FOV, " \
                                                          "go to\n the Folder with same name as the Picture"
                    self.init_interface.resultFOV.config(text=result)
            else:
                pass
        except:
            pass

    # Loop to show the Driectogram for the given Picture and to which picture it belongs
    def resultDirLoop(self):
        if self.DirDone == 1:
            selectedPf = self.returnSelectedPictures()
            for filename in selectedPf:
                os.chdir(os.path.dirname(os.path.abspath(filename)))
                try:

                    # Fix the Filename and path, so i can read from the Folder where the Results are saved
                    tempPath = filename[:-3]
                    pngPath = tempPath + " - Directogram"
                    os.chdir(pngPath)
                    file = ntpath.basename(filename)
                    result = "Results for Directogramm: " + file
                    self.init_interface.resultDir.config(text=result)
                    file = file[:-3]
                    imagePath = file + "1-explosion.png"

                    img = Image.open(imagePath)
                    img = img.resize((400, 400), Image.ANTIALIAS)
                    pngImage = ImageTk.PhotoImage(img)
                    self.init_interface.resultLabelDir.destroy()
                    self.init_interface.resultLabelDir = Label(self.init_interface, image=pngImage,
                                                               relief=GROOVE)
                    self.init_interface.resultLabelDir.image = pngImage
                    self.init_interface.resultLabelDir.place(x="700", y="260")
                except Exception as err:
                    print("The Matlab Process ist not finished yet, therefore there is no Image to open")
                    print(Exception, err)
        else:
            pass

    # The Directogram Script (to implement)
    def startDirectogramScript(self):
        if self.callDir == 1:
            selectedPf = self.returnSelectedPictures()
            if self.callFOV == 0:
                if len(selectedPf) == 0:
                    self.infoBoxSelected()
            for filename in selectedPf:
                # Set the path to the folder where the matlab script is located
                os.chdir(os.path.dirname(os.path.abspath(__file__)))
                # Split the path to get just the name of file because is needed for the Script
                file = ntpath.basename(filename)

                # /Applications/MATLAB_R2021a.app(167) ist the Path to my (Florent Kqiku) MATLAB-Application
                # To use the Script use your own Path to MATLAB or MATLAB-Runtime in your Computer
                p = subprocess.Popen(["./run_LMKFisheye_Tregenza.sh",
                                      "/Applications/MATLAB_R2021a.app", file, filename])
                # Wait for Process to finish
                p.communicate()
                self.DirDone = 1
                self.resultDirLoop()

        else:
            pass

    # Show infoBox if no file selected from Listbox before pressing Evaluate
    def infoBoxSelected(self):
        tk.messagebox.showinfo("Information", "You did not select a picture, pls selected a Picture first then "
                                              "press the Evaluate Button")

    # Runs the script for the Restricted Field of Views
    def startFOVScript(self):
        if self.callFOV == 1:
            selectedPf = self.returnSelectedPictures()
            upsidedown = self.checkVar3
            if len(selectedPf) == 0:
                self.infoBoxSelected()
            fs.startFOVScript(selectedPf, upsidedown)
            self.FOVDone = 1
            self.resultFOVLoop()

    # This Method sets the Visuals, Button, Labels etc. for the GUI-Window
    def setInterface(self):
        # Create Application with given size and Name
        self.init_interface.title("Lichttechnik - Auswertung von .pf Bildern")
        self.init_interface.geometry("1200x720")
        self.init_interface.resizable(False, False)

        # Welcome Message
        self.init_interface.welMsg = Message(self.init_interface, text="Welcome to the GUI for evaluating .pf Pictures",
                                             width="800")
        self.init_interface.welMsg.pack()

        # Buttons for importing .pf Files
        self.init_interface.impButton = tk.Button(self.init_interface,
                                                  text="Search File", command=self.openFile,
                                                  activeforeground="black", activebackground="black")
        self.init_interface.impButton.place(x="100", y="80")

        # Show the name of the chosen File
        self.init_interface.filenameListbox = tk.Listbox(self.init_interface, width=70, height=9,
                                                         selectmode=MULTIPLE)
        self.init_interface.filenameListbox.insert(1, "No file selected yet...")
        self.init_interface.filenameListbox.place(x=200, y=40)

        # Button to close the interface window
        self.init_interface.closeWindow = tk.Button(self.init_interface,
                                                    text="Close window", command=self.closeWindow)
        self.init_interface.closeWindow.pack(side=BOTTOM, fill=BOTH)

        # Button to continue after choosing Picture
        self.init_interface.continueButton = tk.Button(self.init_interface,
                                                       text="Evaluate picture", command=self.setWhichScriptToCall,
                                                       state=DISABLED)
        self.init_interface.continueButton.pack(side=BOTTOM, fill=BOTH)

        # Checkboxes for choosing between Directogram & Restricted FOV
        self.init_interface.checkBtn1 = Checkbutton(self.init_interface,
                                                    text="Directogram", variable=self.checkVar1, offvalue=0, onvalue=1,
                                                    command=self.activateEvalButton, state=DISABLED)
        self.init_interface.checkBtn1.place(x="850", y="80")

        self.init_interface.checkBtn2 = Checkbutton(self.init_interface,
                                                    text="Restricted Field of Views", variable=self.checkVar2,
                                                    offvalue=0, onvalue=1, command=self.activateEvalButton,
                                                    state=DISABLED)
        self.init_interface.checkBtn2.place(x="1000", y="80")

        # Checkbutton for choosing the rotation of the picture upside down
        self.checkVar3.set(False)
        self.init_interface.checkBtn3 = tk.Checkbutton(self.init_interface,
                                                       text="Upsidedown", variable=self.checkVar3,
                                                       command=self.upsidedown)
        self.init_interface.checkBtn3.place(x="1000", y="110")

        # Defines Label for the Result of the calculated FOV
        self.init_interface.resultFOV = Label(text="Results for FOV:", relief=SUNKEN)
        self.init_interface.resultFOV.place(x="100", y="210")
        self.init_interface.resultLabelFOV = Label(self.init_interface, text="Not calculated yet.", relief=GROOVE)
        self.init_interface.resultLabelFOV.place(x="100", y="290")

        # InfoMessage for the FOV Result Box
        # self.init_interface.infMsgResFOV = Message(self.init_interface,
        #                                            text="", width="400", justify="center")
        # self.init_interface.infMsgResFOV.place(x="100", y="350")

        # Defines Label for the Driectogramm
        self.init_interface.resultDir = Label(text="Results for Directogramm:", relief=SUNKEN)
        self.init_interface.resultDir.place(x="700", y="210")
        self.init_interface.resultLabelDir = Label(self.init_interface, text="Not calculated yet.", relief=GROOVE)
        self.init_interface.resultLabelDir.place(x="700", y="290")


# The following function is based on the function from nguen, but changed for my Task
# since i need to use his calculations
def startInterface():
    start = tk.Tk()
    imageProcessing = ip.ImageProcessing()
    interface = Interface(start, imageProcessing)
    interface.setInterface()
    interface.resultFOVLoop()
    start.mainloop()
    fname = interface.fname
    upsidedown = interface.upsidedown
    return fname, upsidedown
