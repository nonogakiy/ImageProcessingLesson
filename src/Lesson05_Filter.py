import cv2
import math

blurSize : int = 0
medianSize : int = 0
gaussSize = 0.0

def onBlurSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = math.floor(pos / 8)
    medianSize = 0
    gaussSize = 0.0

def onMedianSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = 0
    medianSize = math.floor(pos / 8 ) * 2 + 1
    gaussSize = 0.0

def onGaussSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = 0
    medianSize = 0
    gaussSize = pos / 255 * 20

empire_photo = cv2.imread('./data/empire.jpg')

cv2.imshow('FilterTest', empire_photo)
cv2.createTrackbar('Blur', 'FilterTest', 0, 255, onBlurSizeChanged)
cv2.createTrackbar('Median', 'FilterTest', 0, 255, onMedianSizeChanged)
cv2.createTrackbar('Gauss', 'FilterTest', 0, 255, onGaussSizeChanged)

while True:
    if blurSize != 0:
        disp = cv2.blur(empire_photo, (int(blurSize), int(blurSize)))
        cv2.setTrackbarPos('Median', 'FilterTest', 0)
        cv2.setTrackbarPos('Gauss', 'FilterTest', 0)
    elif medianSize != 0:
        disp = cv2.medianBlur(empire_photo, int(medianSize))
        cv2.setTrackbarPos('Blur', 'FilterTest', 0)
        cv2.setTrackbarPos('Gauss', 'FilterTest', 0)
    elif gaussSize != 0.0:
        disp = cv2.GaussianBlur(empire_photo, (31,31), gaussSize, borderType = cv2.BORDER_DEFAULT)
        cv2.setTrackbarPos('Blur', 'FilterTest', 0)
        cv2.setTrackbarPos('Median', 'FilterTest', 0)
    else:
        disp = empire_photo
    
    cv2.imshow('FilterTest', disp)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

cv2.destroyAllWindows()