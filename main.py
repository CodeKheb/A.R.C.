import sys
import time
import pygame
import cv2
import threading

from PyQt6.QtWidgets import QApplication

import core.audio as audio
import core.speech as speech
import utils.process_utils as process
import core.gestures as gestures
import core.camera as cam

from gui.main_window import MainWindow
from config import SNAP_COOLDOWN

app = QApplication(sys.argv)
threading.Thread(target=speech.listen, daemon=True).start()

def draw_hands(frame, hand):
        thumb = hand[4]
        middle = hand[12]
        thumb_x, thumb_y = int(thumb.x * frame.shape[1]), int(thumb.y * frame.shape[0])
        middle_x, middle_y = int(middle.x * frame.shape[1]), int(middle.y * frame.shape[0])
        cv2.line(frame, (thumb_x, thumb_y), (middle_x, middle_y), (0, 255, 0), 2)


def process_camera():
    # detection for clap, camera toggle (indentation nightmare)
    if audio.clap_detected:
        cam.toggle_camera()
        audio.clap_detected = False

    cmd = speech.get_voice_command()
    if cmd:
        if "snap" in cmd.lower() or "open" in cmd.lower():
            print(f"Voice: {cmd}")
            process.open_neovim()
        elif "right" in cmd.lower():
            print(f"Voice: {cmd}")
            process.window_right()
        elif "left" in cmd.lower():
            print(f"Voice: {cmd}")
            process.window_left()
        elif "close" in cmd.lower():
            print(f"Voice: {cmd}")
            process.close_window()

    # process video while camera on
    if not cam.camera_on or cam.cap is None:
        pygame.mixer.music.stop()
        return None

    ret, frame = cam.cap.read()
    if not ret or frame is None:
        return None


    result = cam.convert_colors(frame)

        # draw landmarks on frame
    if result.hand_landmarks:
        for hand in result.hand_landmarks:

            if gestures.detect_snap(hand):
                current_time = time.time()

                if current_time - gestures.last_snap > SNAP_COOLDOWN:
                    print("SNAPPED")
                    process.close_window()
                    gestures.last_snap = current_time

            direction = gestures.get_horizontal_direction(hand)
                    
            if direction == "right":
                print("MOVED RIGHT")
                process.window_right()

            if direction == "left":
                print("MOVED LEFT")
                process.window_left()


            for lm in hand:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 3, (180, 100, 50), -1)

            draw_hands(frame, hand)

    return frame

window = MainWindow(process_camera)
window.show()

exit_code = app.exec()
        
cam.stop_camera()
audio.stream_stop()
app.quit()

sys.exit(exit_code)

