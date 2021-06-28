import time
import cv2
import numpy as np
import matplotlib.pyplot as plt


def calibrate(seconds=60):
    # Connect camera
    cap = cv2.VideoCapture(2)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Camera Connected")
    print("Image Dimensions: ", width, 'x', height)
    print('------------------------------------------')

    # Initialise vars
    frames = 0
    reference = np.zeros((height, width))

    print("Calibration sequence initiated")
    t = time.time()
    # Get feed
    while time.time()-t < seconds:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        reference = reference + frame
        frames += 1

    # Find average noise at each pixel
    reference /= frames
    print("Frames Recorded: ", frames)

    # Release capture
    cap.release()

    # Crop reference image to 360x480, using only usable pixels
    crop = reference[120:, :480]

    return reference, crop


def setThreshold(ref):
    print("Maximum Average Pixel Noise : ", np.max(ref))
    tres = float(input("Enter Minimum Threshold: "))
    return tres


def plot(ref, crop):
    img = ref / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('calibration_map_full.png')
    img = crop / 255.0
    plt.imshow(img, cmap='gray')
    plt.savefig('calibration_map_crop.png')


if __name__ == '__main__':
    foo, too = calibrate(10)
    # print(setThreshold(foo))
    plot(foo, too)
