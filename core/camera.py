import cv2
import core.audio as audio
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from typing import Optional


base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

# options 2 hands for HandLandmarkerOptions
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)

# detector
detector = vision.HandLandmarker.create_from_options(options)

cap: Optional[cv2.VideoCapture] = None
camera_on = False

print("clap")

def stop_camera():
    global cap, camera_on
    if cap is not None:
        cap.release()
        cap = None

    camera_on = False

def toggle_camera():
    global cap, camera_on

    audio.clap_detected = False

    if not camera_on:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            cap = None
        else:
            camera_on = True

    else:
        stop_camera()



def convert_colors(frame):
        # Convert BGR (OpenCV) to RGB (MediaPipe)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # detect landmarks
        result = detector.detect(mp_image)

        return result

