from .calibration import calibrate, setThreshold
from .checkIslands import calculate
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
from tinydb import TinyDB


def setup():
    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists('images/raw_frame'):
        os.mkdir('images/raw_frame')
    if not os.path.exists('images/processed_frame'):
        os.mkdir('images/processed_frame')
    if not os.path.exists('images/map_frame'):
        os.mkdir('images/map_frame')


def start(seconds=10, duration=60):
    reference, calibration_crop = calibrate(seconds)
    print("Calibration sequence completed")
    print('------------------------------------------')

    min_value = setThreshold(calibration_crop)
    tres_matrix = np.ones(calibration_crop.shape) * min_value

    # Connect camera
    cap = cv2.VideoCapture(2)
    frames = 0

    print("Starting collecting readings")
    start_time = time.time()
    # Get readings
    while (time.time() - start_time < duration):
        try:
            # Get Camera Input
            ret, frame = cap.read()
            t = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames += 1

            # Crop to usable part
            crop = frame[120:, :480]

            # Get actual input after subtraction
            temp = crop - calibration_crop - tres_matrix
            temp = np.clip(temp, 0, 255)

            # Check for islands on subtracted frame
            islands, maxArea, bmp = calculate(temp)

            # Add entry in db if island exists and > 5 pixels
            if maxArea > 5:
                post(islands, maxArea, t, frame, temp, min_value, bmp)

        except KeyboardInterrupt:
            # Release capture
            cap.release()
            break
    print("Ran for {} frames".format(frames))


def save(raw, processed, bmp, t):
    # Save Raw Image
    img = raw / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/raw_frame/{}.png'.format(t))
    # Save Processed Image
    img = processed / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/processed_frame/{}.png'.format(t))
    # Save Island Bitmap
    img = bmp / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('images/map_frame/{}.png'.format(t))


def post(islands, area, t, raw, processed, min_value, bmp):
    save(raw, processed, bmp, t)
    db = TinyDB('db.json')
    data = {
        'time': t,
        'area': area,
        'islands': islands,
        'threshold': min_value,
        'frame': 'images/raw_frame/{}.png'.format(t),
        'processed': 'images/processed_frame/{}.png'.format(t),
        'bmp': 'images/map_frame/{}.png'.format(t)
    }
    print('------------------------------------------')
    print(data)
    db.insert(data)


if __name__ == '__main__':
    setup()
    start()
