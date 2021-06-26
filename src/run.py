from calibration import calibrate, setThreshold
import numpy as np
import cv2
import requests
import os


def setup():
    if not os.path.exists('images'):
        os.mkdir('images')


def start(seconds=10):
    calibration_frame = calibrate(seconds)
    print("Calibration sequence completed")
    min_value = setThreshold(calibration_frame)
    tres_matrix = np.ones((480, 640)) * min_value
    # Connect camera
    cap = cv2.VideoCapture(2)
    frames = 0

    # Get readings
    while True:
        try:
            # Get Camera Input
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames += 1
            # Get actual input after subtraction
            temp = frame - calibration_frame - tres_matrix
            temp = np.clip(temp, 0)

        except KeyboardInterrupt:
            # Release capture
            cap.release()


def post():
    pass


if __name__ == '__main__':
    pass
