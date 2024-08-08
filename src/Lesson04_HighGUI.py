import cv2

empire_photo = cv2.imread('./data/empire.jpg')
cv2.imshow('HighGUI Test', empire_photo)

def onTrackbarEvent(pos):
    print('trackbar: %d'% pos)

def onMouseEvent(event, x, y, flag, param):
    print('(%d, %d)'%(x, y))

init_pos = 128
cv2.setMouseCallback('HighGUI Test', onMouseEvent)
cv2.createTrackbar('trackbar', 'HighGUI Test', init_pos, 255, onTrackbarEvent)

cv2.waitKey(0)

cv2.destroyAllWindows()