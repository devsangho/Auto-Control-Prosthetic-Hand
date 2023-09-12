import numpy as np
from scipy.spatial.transform import Rotation as R

def get_head_angle(camera_angle, imu_angle):
    r_x, r_y, r_z = camera_angle
    camera_angle = np.array([r_z, -r_x, r_y])
    rotation_matrix = np.matmul(imu_angle, camera_angle)
    rotation_matrix = R.from_matrix(rotation_matrix)
    # x, y, z = rotation_matrix.as_rotvec().as_euler("xyz", degrees=True)
    x, y, z = rotation_matrix.as_euler("xyz", degrees=True)
    return z


def get_hand_angle(angle):
    return 90 + angle
