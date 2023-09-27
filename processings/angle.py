import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp


def get_head_angle(camera_angle, imu_angle):
    # axis_rotation_matrix = np.array([[0,0,-1],
    #                                  [-1,0,0],
    #                                  [0,1,0],])
    # object_rotation_matrix = np.matmul(imu_angle, axis_rotation_matrix)
    # object_rotation_matrix = np.matmul(object_rotation_matrix, camera_angle)
    # object_rotation_matrix = np.matmul(object_rotation_matrix, camera_angle)
    # object_rotation_matrix = np.matmul(object_rotation_matrix, axis_rotation_matrix.T)

    imu_rotation = R.from_matrix(imu_angle)
    axis_rotation_matrix = np.array([[0,0,-1],
                                     [-1,0,0],
                                     [0,1,0],])
    axis_rotation = R.from_matrix(axis_rotation_matrix)
    identity_rotation = R.identity()
    objectron_rotation = R.from_matrix(camera_angle)

    squared_objectron_rotaion = objectron_rotation * objectron_rotation
    rotations = R.concatenate([identity_rotation, squared_objectron_rotaion])
    key_times = [0, 2]
    slerp = Slerp(key_times, rotations)
    interpolated_rotation = slerp(1)

    object_rotation = imu_rotation * axis_rotation * interpolated_rotation * axis_rotation.inv()
    object_rotation_matrix = object_rotation.as_matrix()

    rotation_vector = object_rotation_matrix[:,2]
    rotation_vector = [0, rotation_vector[1], rotation_vector[2]]
    rotation_vector = rotation_vector/np.linalg.norm(rotation_vector)
    print(rotation_vector)

    angle = -np.arctan(object_rotation_matrix[1,2]/object_rotation_matrix[2,2])/3.1415*180

    return angle

def get_hand_angle(angle):
    return 90 + angle
