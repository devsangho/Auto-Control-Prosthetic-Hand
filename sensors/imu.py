from teensy import arduino1
from processings.angle import get_rotation_matrix_from_quaternion
import numpy as np
from collections import deque


class ImuAndEmg:
    def __init__(self):
        self.rotation_matrix = None
        self.emglist_max_length = 125
        self.emglist_ch1 = deque([], maxlen=self.emglist_max_length)
        self.emglist_ch2 = deque([], maxlen=self.emglist_max_length)

    def run(self):
        print("IMU running...")
        arduino1.send("START_IMU_AND_EMG")

        while arduino1.arduino.readable():
            arduino1.arduino.reset_input_buffer()
            arduino1.arduino.reset_output_buffer()

            raw_response = arduino1.arduino.readline()
            response = raw_response[0 : len(raw_response) - 1].decode().split("\t")

            # quat 값만 주어지는 경우
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

            # emg 신호만 주어지는 경우
            if response[0] == "emg":
                self.emglist_ch1.append(float(response[1]))
                self.emglist_ch2.append(float(response[2]))

            # quat 값과 emg 신호가 함께 주어지는 경우
            if len(response) == 8 and response[5] == "emg":
                self.emglist_ch1.append(float(response[6]))
                self.emglist_ch2.append(float(response[7]))
