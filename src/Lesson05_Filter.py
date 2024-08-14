import cv2

blurSize = 0.0
medianSize = 0.0
gaussSize = 0.0

def onBlurSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = pos / 255 * 5
    medianSize = 0.0
    gaussSize = 0.0

def onMedianSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = 0.0
    medianSize = pos / 255 * 5
    gaussSize = 0.0

def onGaussSizeChanged(pos):
    global blurSize
    global medianSize
    global gaussSize
    blurSize = 0.0
    medianSize = 0.0
    gaussSize = pos / 255 * 5

empire_photo = cv2.imread('./data/empire.jpg')

cv2.imshow('FilterTest', empire_photo)
cv2.createTrackbar('Blur', 'FilterTest', 0, 255, onBlurSizeChanged)
cv2.createTrackbar('Median', 'FilterTest', 0, 255, onMedianSizeChanged)
cv2.createTrackbar('Gauss', 'FilterTest', 0, 255, onGaussSizeChanged)

while True:
    if blurSize != 0.0:
        disp = cv2.blur(empire_photo, (blurSize,blurSize), (-1,-1), cv2.BORDER_DEFAULT )
        cv2.setTrackbarPos('Median', 'FilterTest', medianSize)
        cv2.setTrackbarPos('Gauss', 'FilterTest', gaussSize)
    elif medianSize != 0.0:
        disp = cv2.medianBlur(empire_photo, (medianSize,medianSize))
        cv2.setTrackbarPos('Blur', 'FilterTest', blurSize)
        cv2.setTrackbarPos('Gauss', 'FilterTest', gaussSize)
    elif gaussSize != 0.0:
        disp = cv2.GaussianBlur(empire_photo, (11,11), gaussSize, borderType = cv2.BORDER_DEFAULT)
        cv2.setTrackbarPos('Blur', 'FilterTest', blurSize)
        cv2.setTrackbarPos('Median', 'FilterTest', medianSize)
    else:
        disp = empire_photo
    
    cv2.imshow('FilterTest', disp)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

cv2.destroyAllWindows()