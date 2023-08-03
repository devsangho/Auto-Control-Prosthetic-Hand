from teensy import arduino1
from processings.angle import get_rotation_matrix_from_quaternion
import numpy as np


class IMU:
    def __init__(self):
        self.rotation_matrix = None

    def run(self):
        print("IMU running...")
        arduino1.send("START_IMU")
        while arduino1.arduino.readable():
            raw_response = arduino1.arduino.readline()
            response = raw_response[0 : len(raw_response) - 1].decode().split("\t")

            if response[0] == "quat":
                quat = [
                    float(response[1]),
                    float(response[2]),
                    float(response[3]),
                    float(response[4]),
                ]
                self.rotation_matrix = np.array(
                    get_rotation_matrix_from_quaternion(quat)
                )
