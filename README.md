# WebCam-Cosmic-Rays
Using webcams to detect cosmic rays.

## Usage:
Step 1 : Create a virtual environment with `python3 -m venv env`, and activate it with `. env/bin/activate` (Linux)

Step 2 : Install requirements in the virtual environment with `pip install -r requirements.txt`

Step 3: Run `python3 start.py` from the command line to start.

Step 4 : Input time (in seconds) to calibrate the setup.

Step 5 : Input time (in seconds) to take observations.

## Basic Troubleshooting:
Check your webcam's id to ensure the correct input device is being read. You might have to change the `cv2.VideoCapture(2)` line in the `calibration.py`, `run.py` and `testImageCapture.py` scripts.

## Hardware Setup
- 2 x Sunfeast Dark Fantasy Boxes
- 1 x Logitech C110 640x480 USB Webcam
- Tape

***Ensure the webcam is in complete darkness, and seal all holes light can leak through from with tape.***

<img src = "https://github.com/Naimish240/WebCam-Cosmic-Rays/blob/main/Assets/1.jpg" width=250>
<img src = "https://github.com/Naimish240/WebCam-Cosmic-Rays/blob/main/Assets/2.jpg" width=250>
<img src = "https://github.com/Naimish240/WebCam-Cosmic-Rays/blob/main/Assets/3.jpg" width=250>

## Principle
When a cosmic ray enters the CMOS sensor the cosmic ray deposits a charge onto the sensor itself. If the sensor is not exposed to any sources of light, the cosmic ray will leave a track behind in the resulting image.

## Implementation
The cosmic ray is identified through a multi step process. Analysis is performed on an image-by-image basis. The steps are as follows:

### Step 1: Calibration
Most digital cameras these days make use of CMOS sensors to take images. Being digital sensors, they are susceptible to external interference which manifests itself as "noise" in the image. Hence, we first need to identify the average noise in each pixel of the sensor.

The average noise in the image is obtained in the form of a "calibration frame", and we subtract its value from each and every image. Next, we set a threshold value. All pixels with a brightness greater than this threshold are then considered for the next step.

### Step 2 : Island Identification
The image from the previous step is converted into a simple black and white image, with each pixel having a value of either "0" or "1", depending on whether the sensor was activated at that pixel or not. Then, we find all "islands" and their corresponding sizes (LeetCode problem attached in References). If the image has islands with size greater than 5 pixels (to avoid random hot pixels)  then move forward to the next step.

### Step 3 : Saving to DB
We store each positive frame from the above step into a simple NoSQL database implemented with TinyDB.

## Results:
Raw Image (Directly from the sensor):

<img src = "https://github.com/Naimish240/WebCam-Cosmic-Rays/blob/main/images/raw_frame/1624906781.0087495.png" height=400>

## To Do:
- Add Bounding Box around each island.
- Implement server stuff for distributed calculations.
- Repeated calibration to account for sensor heating every 2-3 hours.
- Link with another webcam to identify direction the ray is coming from, and then verify special relativity.

## References
- https://via.library.depaul.edu/cgi/viewcontent.cgi?referer=https://www.google.com/&httpsredir=1&article=1021&context=ahac
- https://credo.science/
- https://wipac.wisc.edu/deco/home
- https://github.com/credo-science/Credo-detector-for-linux-desktop-and-Raspberry-Pi
- https://leetcode.com/problems/max-area-of-island/
- https://leetcode.com/problems/number-of-islands/
