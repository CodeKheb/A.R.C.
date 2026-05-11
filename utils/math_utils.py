import numpy as np

def calculate_distance(point1, point2):
    # sum numpy shit again
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

