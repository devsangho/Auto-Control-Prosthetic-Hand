import serial
import serial.tools.list_ports
from queue import Queue
from config.teensy import serial_port1, serial_port2, serial_baudrate, timeout
import time
import numpy

ports = serial.tools.list_ports.comports()
print([port.name for port in ports])


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
        self.queue = Queue()

    def send(self, message):
        if type(message) == numpy.float64:
            message = round(message, 2)
        self.queue.put(message)

    def run(self):
        while True:
            if self.queue.empty():
                continue
            message = self.queue.get()
            self.arduino.write("/".encode() + str(message).encode())
            print("message: ", message)

            time.sleep(0.01)
            self.queue = Queue()


arduino1 = Arduino(serial_port=serial_port1)
arduino2 = Arduino(serial_port=serial_port2)
