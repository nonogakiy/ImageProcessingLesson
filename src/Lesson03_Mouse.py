import cv2

empire_photo = cv2.imread('./data/empire.jpg')
cv2.imshow('draw_point', empire_photo)

def onMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(empire_photo, (x, y), 20, (255,0,0), -1)
        print(x, y)
        cv2.imshow('draw_point', empire_photo)

cv2.setMouseCallback('draw_point', onMouseDown)

cv2.waitKey(0)
cv2.destroyAllWindows()