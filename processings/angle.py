import math
import numpy as np


def get_head_angle(camera_angle, imu_angle):
    if camera_angle is None or imu_angle is None:
        return None
    return camera_angle + imu_angle


def get_hand_angle(angle):
    return 90 + angle
