# Test video caputre

import cv2

# USB Webcam
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    cv2.imshow('', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
