import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('cap', frame)

    key = cv2.waitKey(10)
    if key == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()