import math
import numpy as np


def quaternion_to_euler(q):
    (x, y, z, w) = (q[0], q[1], q[2], q[3])

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)

    return [yaw, pitch, roll]


def get_head_angle(camera_angles, imu_angles):
    if camera_angles is None or imu_angles is None:
        return None

    [_, pitch, _] = quaternion_to_euler(imu_angles)
    print("camera_angles", camera_angles, pitch * 100)
    return camera_angles - pitch * 180 / np.pi


def get_hand_angle(angle):
    return 90 - angle
