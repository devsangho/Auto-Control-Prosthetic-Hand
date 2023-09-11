import numpy as np
from collections import deque
from scipy.spatial.transform import Rotation as R


# IMU and EMG data
# emg{ch1},{ch2}quat{w},{x},{y},{z}\n
# emg{ch1},{ch2}\n
class IMUAndEMG:
    def __init__(self):
        self.rotation_matrix = None
        self.emglist_max_length = 125
        self.emglist_ch1 = deque([], maxlen=self.emglist_max_length)
        self.emglist_ch2 = deque([], maxlen=self.emglist_max_length)

    def _split_and_append(self, line):
        line = line.replace("quat", ",").replace("emg", "").split(",")
        self.emglist_ch1.append(float(line[0]))
        self.emglist_ch2.append(float(line[1]))
        return line

    # Save data from buffer_str
    def buffer_to_data(self, buffer_str):
        # Make sure that buffer_str is not truncated
        if buffer_str[0] == "e" and buffer_str[-1] == "\r":
            buffer_list = buffer_str.split("\r")
            del buffer_list[-1]
            buffer_list_length = len(buffer_list)
            if buffer_list_length > self.emglist_max_length:
                buffer_list = buffer_list[
                    buffer_list_length - self.emglist_max_length :
                ]
            # buffer_list = [
            #     line.replace("quat",',').replace("emg",'').split(',') for line in buffer_list
            #     ]
            # for line in buffer_list:
            #     line = line.replace("quat",',').replace("emg",'').split(',')
            #     self.emglist_ch1.append(float(line[0]))
            #     self.emglist_ch2.append(float(line[1]))
            buffer_list = list(map(self._split_and_append, buffer_list))
            for line in reversed(buffer_list):
                if len(line) > 2:
                    quat = [
                        float(line[2]),
                        float(line[3]),
                        float(line[4]),
                        float(line[5]),
                    ]
                    # print(quat)
                    self.rotation_matrix = np.array(R.from_quat(quat).as_matrix())
                    break
