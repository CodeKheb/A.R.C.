import utils.math_utils as math
import config as config

last_snap = 0 # last snap initially zero
previous_x = None

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



def get_horizontal_direction(hand_landmarks):

    global previous_x

    palm_points = [0, 5, 9, 13, 17]

    avg_x = sum(
        hand_landmarks[i].x for i in palm_points
    ) / len(palm_points)

    if previous_x is None:
        previous_x = avg_x
        return None

    delta_x = avg_x - previous_x

    previous_x = avg_x

    if delta_x > config.MOVE_THRESHOLD:
        return "left"

    if delta_x < -config.MOVE_THRESHOLD:
        return "right"

    return None
