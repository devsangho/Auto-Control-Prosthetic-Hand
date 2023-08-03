import numpy as np
import time


def get_rotation_matrix_from_quaternion(Q):
    """
    Covert a quaternion into a full three-dimensional rotation matrix.

    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3)

    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix.
             This rotation matrix converts a point in the local reference
             frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q[0]
    q1 = Q[1]
    q2 = Q[2]
    q3 = Q[3]

    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)

    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)

    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1

    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]])

    return rot_matrix


def get_head_angle(camera_angle, imu_angle):
    r_matrix = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]])
    inverse_of_r_matrix = np.transpose(r_matrix)

    a = np.matmul(imu_angle, r_matrix)  # 월드좌표계 => 카메라좌표계
    b = np.matmul(a, camera_angle)
    c = np.matmul(b, inverse_of_r_matrix)  # 카메라좌표계 => 월드좌표계

    rotation_matrix = c
    z_rotation = np.array(
        [rotation_matrix[0][2], rotation_matrix[1][2], rotation_matrix[2][2]]
    )
    z_rotation_to_yz = np.array([0, z_rotation[1], z_rotation[2]])
    z_unit = np.array([0, 0, 1])

    product = np.dot(z_rotation_to_yz, z_unit)
    z_rotation_norm = np.linalg.norm(z_rotation_to_yz)

    theta_in_radian = np.arccos(np.divide(product, z_rotation_norm))
    theta_in_degree = theta_in_radian * 180 / np.pi

    is_y_vector_positive = z_rotation[1] > 0
    theta_in_degree = -theta_in_degree if is_y_vector_positive else theta_in_degree
    print(
        "time:\n",
        time.time(),
        "theta:\n",
        theta_in_degree,
        "\nrotation_matrix:\n",
        rotation_matrix,
    )
    return theta_in_degree


def get_hand_angle(angle):
    return 90 + angle
