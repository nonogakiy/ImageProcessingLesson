import cv2

gaussSize = 0.0

def onGaussSizeChanged(pos):
    global gaussSize
    gaussSize = pos / 255 * 5

empire_photo = cv2.imread('./data/empire.jpg')

cv2.imshow('FilterTest', empire_photo)
cv2.createTrackbar('Size', 'FilterTest', 0, 255, onGaussSizeChanged

while True:
    if gaussSize == 0:
        disp = empire_photo
    else:
        disp = cv2.GaussianBlur(empire_photo, (11,11), gaussSize, borderType = cv2.BORDER_DEFAULT)

    cv2.imshow('FilterTest', disp)
    key = cv2.waitKey(10)

    if key == ord('q'):
        break

cv2.destroyAllWindows()