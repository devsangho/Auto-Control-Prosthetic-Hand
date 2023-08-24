import serial
import serial.tools.list_ports
from queue import Queue
from config.teensy import serial_port1, serial_port2, serial_baudrate, timeout
import time
import numpy
from scipy.ndimage import gaussian_filter1d
import math

ports = serial.tools.list_ports.comports()
print([port.name for port in ports])


def chunk(lst, size):
    return list(
        map(
            lambda x: lst[x * size : x * size + size],
            # 뒤에서 받은 List를 대입하여 계산한다
            # ex_1) lst[0*3:0*3+3] = lst[0:3] -> list index 0부터 2까지
            # ex_2) lst[1*3:1*3+3] = lst[3:6] -> list index 3부터 5까지
            list(range(0, math.ceil(len(lst) / size)))
            # 받은 lst 길이와 지정된 크기 size를 나누어 올림한 값 = n 이라면,
            # 0부터 n까지의 리스트를 생성한다.
        )
    )


class Arduino:
    def __init__(
        self, serial_port, serial_baudrate=serial_baudrate, timeout=timeout
    ) -> None:
        self.serial_port = serial_port
        self.serial_baudrate = serial_baudrate
        self.time_out = timeout
        self.arduino = serial.Serial(
            port=serial_port, baudrate=serial_baudrate, timeout=timeout
        )
        self.angles = []
        self.hand_positions = []

    def send(self, message):
        if type(message) == numpy.float64:
            message = round(message, 2)
            self.angles.append(message)
        else:
            self.hand_positions.append(message)

    def run(self):
        while True:
            if len(self.angles) > 0:
                smoothed = gaussian_filter1d(self.angles, sigma=50)
                message = smoothed[-1]
                # self.arduino.write("/".encode() + str(message).encode())
                print("message: ", message)
            if len(self.hand_positions) > 0:
                message = self.hand_positions.pop()
                # self.arduino.write("/".encode() + str(message).encode())
                print("message: ", message)


arduino1 = Arduino(serial_port=serial_port1)
# arduino2 = Arduino(serial_port=serial_port2)
