import cv2
import time
import pygame
import subprocess
import os
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
last_clap = 0 # last clap initially zero

clap_detected = False # initially false

last_snap = 0 # last snap initially zero
SNAP_COOLDOWN = 0.5

def calculate_distance(point1, point2):
    # sum numpy shit again
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

def detect_snap(hand_landmarks):
    # MediaPipe landmarks
    thumb_tip = hand_landmarks[4] # 4 is the thumb
    middle_tip = hand_landmarks[12] # 12 for middle finger
    index_tip = hand_landmarks[8] # index

    thumb_middle_dist = calculate_distance(thumb_tip, middle_tip)
    thumb_index_dist = calculate_distance(thumb_tip, index_tip)

    # how close thumb to mid fing 
    SNAP_THRESHOLD = 0.05  # "close" distance
    INDEX_MIN_DIST = 0.08 # thumb should be farther from index

    if thumb_middle_dist < SNAP_THRESHOLD and thumb_index_dist > INDEX_MIN_DIST:
        return True
    return False

def open_neovim():
    try:
        subprocess.Popen(['kitty', '--directory', '~/projects/A.R.C/', 'nvim', '.'])

        print("Welcome home sir!")
    except FileNotFoundError:
        print("kitty not found")
    except Exception as e:
        print(f"Error opening Neovim: {e}")

# audio_callback takes numpy in_data, frames, time_info, status params
def audio_callback(indata, frames, time_info, status):
    # make clap_detected and last global for detection
    global clap_detected, last_clap

    # Print the status of the audio for debug
    if status:
        print(f"Audio status: {status}")

    # sum math numpy shit to calculate volume level
    volume = np.sqrt(np.mean(indata**2))

    # volume detection, if it's less than 0.03
    if volume > THRESHOLD:
        print(f"Volume: {volume:.4f}")

    # volme detection for 0.03 and if time - last is more than 1, detect clap
    if volume > THRESHOLD and time.time() - last_clap > 1:
        print("CLAPPED")

        pygame.mixer.music.load("assets/Back_In_Black.mp3")
        pygame.mixer.music.play()

        clap_detected = True
        last_clap = time.time()

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

def toggle_camera():
    global cap, camera_on, clap_detected
    clap_detected = False
    if not camera_on:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap = None
        else:
            camera_on = True
            cv2.namedWindow("A.R.C. Hello World")
    else:
        stop_camera()

while True:
    # detection for clap, camera toggle (indentation nightmare)
    if clap_detected:
        toggle_camera()

    # process video while camera on
    if camera_on and cap is not None:
        ret, frame = cap.read()
        if not ret or frame is None:
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
                if detect_snap(hand):
                    current_time = time.time()
                    if current_time - last_snap > SNAP_COOLDOWN:
                        print("SNAP")
                        open_neovim()
                        last_snap = current_time

                for lm in hand:
                    x = int(lm.x * frame.shape[1])
                    y = int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 3, (180, 100, 50), -1)

                thumb = hand[4]
                middle = hand[12]
                thumb_x, thumb_y = int(thumb.x * frame.shape[1]), int(thumb.y * frame.shape[0])
                middle_x, middle_y = int(middle.x * frame.shape[1]), int(middle.y * frame.shape[0])
                cv2.line(frame, (thumb_x, thumb_y), (middle_x, middle_y), (0, 255, 0), 2)

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

