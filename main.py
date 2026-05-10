import cv2
import time
import pygame
import sounddevice as sd
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

pygame.mixer.init()

Esc = 27  # KEYCODE FOR ESCAPE

THRESHOLD = 0.03 # Volume needed for clap (usually like 0.1 - 0.3 but my mic low sound af)
SAMPLE_RATE = 44100 # Normal Sample Rate 
BLOCKSIZE = 2048 # Normal blocksize
last = 0 # last clap initially zero

clap_detected = False # initially false

# audio_callback takes numpy in_data, frames, time_info, status params
def audio_callback(indata, frames, time_info, status):
    # make clap_detected and last global for detection
    global clap_detected, last

    # Print the status of the audio for debug
    if status:
        print(f"Audio status: {status}")

    # sum math numpy shit to calculate volume level
    volume = np.sqrt(np.mean(indata**2))

    # volume detection, if it's less than 0.03
    if volume > THRESHOLD:
        print(f"Volume: {volume:.4f}")

    # volme detection for 0.03 and if time - last is more than 1, detect clap
    if volume > THRESHOLD and time.time() - last > 1:
        print("CLAPPED")

        pygame.mixer.music.load("assets/Back_In_Black.mp3")
        pygame.mixer.music.play()

        clap_detected = True
        last = time.time()

# stream audio
stream = sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCKSIZE
        )
# start stream
stream.start()


# mediapipe model asset from wget hand_landmarker.task  
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

cap = None
camera_on = False

print("clap")

def stop_camera():
    global cap, camera_on
    if cap is not None:
        cap.release()
        cap = None
    cv2.destroyAllWindows()
    camera_on = False

while True:

    # detection for clap, camera toggle (indentation nightmare)
    if clap_detected:
        clap_detected = False

        if not camera_on:
            # turn camera_on
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                cap = None
            else:
                camera_on = True
                # cv2 is the camera
                cv2.namedWindow("A.R.C. Hello World")
        else:
            # turn camera off
            stop_camera()

    # process video while camera on
    if camera_on and cap is not None:
        ret, frame = cap.read()

        if not ret:
            time.sleep(0.01)
            continue

        # Convert BGR (OpenCV) to RGB (MediaPipe)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # detect landmarks
        result = detector.detect(mp_image)

        # draw landmarks on frame
        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                for lm in hand:
                    x = int(lm.x * frame.shape[1])
                    y = int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 3, (180, 100, 50), -1)

        cv2.imshow("A.R.C. Hello World", frame)

        # Esc quits too ig
        if cv2.waitKey(1) == Esc:
            stop_camera()
            break
    else:
        pygame.mixer.music.stop()
        time.sleep(0.05)

stream.stop()
stream.close()

