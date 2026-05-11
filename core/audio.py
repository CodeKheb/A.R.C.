import numpy as np
import pygame
import time
import sounddevice as sd
from config import THRESHOLD, BLOCKSIZE, SAMPLE_RATE

last_clap = 0 # last clap initially zero
clap_detected = False # initially false

pygame.mixer.init()


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


def stream_stop():
    stream.stop()
    stream.close()

