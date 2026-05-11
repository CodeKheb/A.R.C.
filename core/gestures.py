import utils.math_utils as math
import config as config

last_snap = 0 # last snap initially zero

def detect_snap(hand_landmarks):
    # MediaPipe landmarks
    thumb_tip = hand_landmarks[4] # 4 is the thumb
    middle_tip = hand_landmarks[12] # 12 for middle finger
    index_tip = hand_landmarks[8] # index

    thumb_middle_dist = math.calculate_distance(thumb_tip, middle_tip)
    thumb_index_dist = math.calculate_distance(thumb_tip, index_tip)

    # how close thumb to mid fing 
    config.SNAP_THRESHOLD = 0.05  # "close" distance
    config.INDEX_MIN_DIST = 0.08 # thumb should be farther from index

    if thumb_middle_dist < config.SNAP_THRESHOLD and thumb_index_dist > config.INDEX_MIN_DIST:
        return True
    return False

