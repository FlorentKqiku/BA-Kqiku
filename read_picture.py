import interface_Window as iw
import array
import numpy as np


# The following function is based on the function from nguen, but changed form my Task
# since i need to use his calculations
def readPicture(fname=None):
    if fname == None:
        filename, upsidedown = iw.startInterface()
    else:
        filename = fname
        upsidedown = False
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
        return imageMatrix, filename, upsidedown
    except:
        pass
