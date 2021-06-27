from calibration import calibrate, setThreshold
from checkIslands import calculate
import numpy as np
import matplotlib.pyplot as plt
import cv2
import requests
import os
import time


def setup():
    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists('images/raw_frame'):
        os.mkdir('images/raw_frame')
    if not os.path.exists('images/processed_frame'):
        os.mkdir('images/processed_frame')
    if not os.path.exists('images/boxed_frame'):
        os.mkdir('images/boxed_frame')


def start(user, seconds=10):
    reference, calibration_crop = calibrate(seconds)
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
            t = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Crop to usable part
            crop = frame[120:, :480]
            frames += 1
            # Get actual input after subtraction
            temp = crop - calibration_crop - tres_matrix
            temp = np.clip(temp, 0)
            # Check for islands on subtracted frame
            islands, area, boxed_frame = calculate(temp)
            # Add entry in db if island exists
            if islands:
                post(islands, area, t, frame, temp, boxed_frame, user)
        except KeyboardInterrupt:
            # Release capture
            cap.release()


def save(frame, temp, boxed_frame, t):
    img = frame / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/raw_frame/{}.png'.format(t))
    img = temp / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/processed_frame/{}.png'.format(t))
    img = boxed_frame / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/boxed_frame/{}.png'.format(t))


def post(islands, area, t, frame, temp, boxed_frame, user):
    save(frame, temp, boxed_frame, t)


if __name__ == '__main__':
    pass
