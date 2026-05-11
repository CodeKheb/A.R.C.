import time
import pygame
import cv2

import core.audio as audio
import utils.process_utils as process
import core.gestures as gestures
import core.camera as cam

from config import Esc, SNAP_COOLDOWN


while True:
    # detection for clap, camera toggle (indentation nightmare)
    if audio.clap_detected:
        cam.toggle_camera()

    # process video while camera on
    if cam.camera_on and cam.cap is not None:
        ret, frame = cam.cap.read()
        if not ret or frame is None:
            time.sleep(0.01)
            continue


        result = cam.convert_colors(frame)

        # draw landmarks on frame
        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                if gestures.detect_snap(hand):
                    current_time = time.time()
                    if current_time - gestures.last_snap > SNAP_COOLDOWN:
                        print("SNAP")
                        process.open_neovim()
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
            cam.stop_camera()
            break
    else:
        pygame.mixer.music.stop()
        time.sleep(0.05)

audio.stream_stop()
