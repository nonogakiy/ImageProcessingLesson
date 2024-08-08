import cv2

empire_photo = cv2.imread('./data/empire.jpg')
cv2.imshow('FilterTest', empire_photo)

cv2.waitKey(0)

empire_photo = cv2.GaussianBlur(empire_photo, (5,5), sigmaX = 10.0, sigmaY = 10.0, borderType = cv2.BORDER_DEFAULT)
cv2.imshow('FilterTest', empire_photo)
cv2.waitKey(0)

cv2.destroyAllWindows()