import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp


def get_head_angle(camera_angle, imu_angle):
    convert_axis = np.array(
        [
            [0, 0, -1],
            [-1, 0, 0],
            [0, 1, 0],
        ]
    )
    imu_angle = np.multiply(imu_angle, convert_axis)
    objectron_matrix = np.multiply(camera_angle, camera_angle)
    rotation_matrix = np.multiply(imu_angle, objectron_matrix)
    rotation_matrix = np.multiply(objectron_matrix, np.transpose(convert_axis))

    _, _, z = R.from_matrix(rotation_matrix).as_euler("xyz", degrees=True)
    return z


def get_hand_angle(angle):
    return 90 + angle
