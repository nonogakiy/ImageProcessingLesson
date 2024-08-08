import cv2

empire_photo = cv2.imread('./data/empire.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Empire', empire_photo)

cv2.waitKey(0)
cv2.destroyAllWindows()
