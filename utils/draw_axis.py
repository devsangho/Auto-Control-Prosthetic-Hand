import cv2
import numpy as np
from typing import Tuple

RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)


def imu_draw_axis(image, rotation_matrix,
                  focal_length: Tuple[float, float] = (1.0, 1.0),
                  principal_point: Tuple[float, float] = (0.0, 0.0),
                  axis_length: float = 0.15):
    
    image_rows, image_cols, _ = image.shape
    # Create axis points in camera coordinate frame.
    axis_world = np.float32([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # Move camera view point according to drawing coordinate.
    translation_matrix = np.array([-0.3, 0., 0.])
    
    # Draw rotation axis.
    axis_cam = np.matmul(rotation_matrix, axis_length * axis_world.T).T + translation_matrix
    x = axis_cam[..., 0]
    y = axis_cam[..., 1]
    z = axis_cam[..., 2]
    # Project 3D points to NDC space.
    fx, fy = focal_length
    px, py = principal_point
    y_ndc = np.clip(fx * y / ((-x) + 1e-5) + px, -1., 1.)
    z_ndc = np.clip(fy * z / ((-x) + 1e-5) + py, -1., 1.)
    # Convert from NDC space to image space.
    x_im = np.int32((1 - y_ndc) * 0.5 * image_cols)
    y_im = np.int32((1 - z_ndc) * 0.5 * image_rows)
    # Draw xyz axis on the image.
    origin = (x_im[0], y_im[0])
    x_axis = (x_im[1], y_im[1])
    y_axis = (x_im[2], y_im[2])
    z_axis = (x_im[3], y_im[3])
    cv2.arrowedLine(image, origin, x_axis, RED_COLOR, 3)
    cv2.arrowedLine(image, origin, y_axis, GREEN_COLOR, 3)
    cv2.arrowedLine(image, origin, z_axis, BLUE_COLOR, 3)

    # Draw base axis.
    axis_base = np.matmul(np.identity(3), axis_length * axis_world.T).T + translation_matrix
    x = axis_base[..., 0]
    y = axis_base[..., 1]
    z = axis_base[..., 2]
    # Project 3D points to NDC space.
    fx, fy = focal_length
    px, py = principal_point
    y_ndc = np.clip(fx * y / ((-x) + 1e-5) + px, -1., 1.)
    z_ndc = np.clip(fy * z / ((-x) + 1e-5) + py, -1., 1.)
    # Convert from NDC space to image space.
    x_im = np.int32((1 - y_ndc) * 0.5 * image_cols)
    y_im = np.int32((1 - z_ndc) * 0.5 * image_rows)
    # Draw xyz axis on the image.
    origin = (x_im[0], y_im[0])
    x_axis = (x_im[1], y_im[1])
    y_axis = (x_im[2], y_im[2])
    z_axis = (x_im[3], y_im[3])
    cv2.arrowedLine(image, origin, x_axis, RED_COLOR, 3)
    cv2.arrowedLine(image, origin, y_axis, GREEN_COLOR, 3)
    cv2.arrowedLine(image, origin, z_axis, BLUE_COLOR, 3)

    return image

def objectron_draw_axis(image, rotation_matrix,
                        focal_length: Tuple[float, float] = (1.0, 1.0),
                        principal_point: Tuple[float, float] = (0.0, 0.0),
                        axis_length: float = 0.15):

    image_rows, image_cols, _ = image.shape
    # Create axis points in camera coordinate frame.
    axis_world = np.float32([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # Move camera view point according to drawing coordinate.
    translation_matrix = np.array([0., 0., 0.3])
    
    # Draw rotation axis.
    axis_cam = np.matmul(rotation_matrix, axis_length * axis_world.T).T + translation_matrix
    x = axis_cam[..., 0]
    y = axis_cam[..., 1]
    z = axis_cam[..., 2]
    # Project 3D points to NDC space.
    fx, fy = focal_length
    px, py = principal_point
    x_ndc = np.clip(fx * x / (z + 1e-5) + px, -1., 1.)
    y_ndc = np.clip(fy * y / (z + 1e-5) + py, -1., 1.)
    # Convert from NDC space to image space.
    x_im = np.int32((1 + x_ndc) * 0.5 * image_cols)
    y_im = np.int32((1 - y_ndc) * 0.5 * image_rows)
    # Draw xyz axis on the image.
    origin = (x_im[0], y_im[0])
    x_axis = (x_im[1], y_im[1])
    y_axis = (x_im[2], y_im[2])
    z_axis = (x_im[3], y_im[3])
    cv2.arrowedLine(image, origin, x_axis, RED_COLOR, 3)
    cv2.arrowedLine(image, origin, y_axis, GREEN_COLOR, 3)
    cv2.arrowedLine(image, origin, z_axis, BLUE_COLOR, 3)

    # Draw base axis.
    axis_base = np.matmul(np.identity(3), axis_length * axis_world.T).T + translation_matrix
    x = axis_base[..., 0]
    y = axis_base[..., 1]
    z = axis_base[..., 2]
    # Project 3D points to NDC space.
    fx, fy = focal_length
    px, py = principal_point
    x_ndc = np.clip(fx * x / (z + 1e-5) + px, -1., 1.)
    y_ndc = np.clip(fy * y / (z + 1e-5) + py, -1., 1.)
    # Convert from NDC space to image space.
    x_im = np.int32((1 + x_ndc) * 0.5 * image_cols)
    y_im = np.int32((1 - y_ndc) * 0.5 * image_rows)
    # Draw xyz axis on the image.
    origin = (x_im[0], y_im[0])
    x_axis = (x_im[1], y_im[1])
    y_axis = (x_im[2], y_im[2])
    z_axis = (x_im[3], y_im[3])
    cv2.arrowedLine(image, origin, x_axis, RED_COLOR, 3)
    cv2.arrowedLine(image, origin, y_axis, GREEN_COLOR, 3)
    cv2.arrowedLine(image, origin, z_axis, BLUE_COLOR, 3)

    return image
