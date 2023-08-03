from processings.angle import get_head_angle
import numpy as np
import torch
import cv2
from worker import Worker
from models.objectron.model import Objectron
from models.hand_landmark_detection.model import HandLandmarkDetection
import numpy as np

from teensy import arduino1, arduino2
from processings import hand, angle
from sensors.imu import IMU

import time


imu = IMU()
imu_thread = Worker(name="imu", model=imu)

arduino1_thread = Worker(name="arduino1", model=arduino1)
arduino2_thread = Worker(name="arduino2", model=arduino2)

arduino1_thread.start()
arduino2_thread.start()
imu_thread.start()

while True:
    if imu.rotation_matrix is not None:
        get_head_angle(
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            imu.rotation_matrix,
        )
