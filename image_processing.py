# Update: 10.11.2021
# Update for the Purpose of a GUI in the Bachelor Thesis of Florent Kqiku
# The updates involve sourcing the Code for calculations to other files,
# so the Code here is just to start the GUI
# The Name was also Updated
# Update-Author: Florent Kqiku


import read_picture as rp


class ImageProcessing:
    def __init__(self):
        print('Starting GUI ')


if __name__ == '__main__':
    im, fpath, upsidedown = rp.readPicture()
