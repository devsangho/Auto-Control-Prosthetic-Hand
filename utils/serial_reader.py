import serial
import serial.tools.list_ports
from queue import Queue
import threading, time
import numpy


ports = serial.tools.list_ports.comports()
print([port.name for port in ports])

# Bufferless Serial
# https://stackoverflow.com/questions/1093598/pyserial-how-to-read-the-last-line-sent-from-a-serial-device
class Serial:
    def __init__(self, port, baudrate=115200, timeout=0, write_timeout=0, is_reading=False):
        self.ser = serial.Serial(
            port=port, baudrate=baudrate, timeout=timeout, write_timeout=write_timeout
        )
        if is_reading == True:
            self.FREQ = 500 #Hz
            self.buffer_str = ""
            self.lock = threading.Lock()
            t = threading.Thread(target=self._reader)
            t.daemon = True
            self.ser.reset_input_buffer()
            t.start()

    def _reader(self):
        while True:
            with self.lock:
                buffer_bytes = self.ser.read(self.ser.in_waiting)
            buffer_str = buffer_bytes.decode('ascii')
            # for debug
            # print(buffer_str, end='end\n')
            self.buffer_str += buffer_str
            # Prevent threading loop from running to fast
            time.sleep(1/self.FREQ)

    def write(self, message_str):
        # time1 = time.time()
        message_bytes = (message_str+'\r\n').encode('utf-8')
        bytes_written = self.ser.write(message_bytes)
        if bytes_written != len(message_bytes):
            print("Message truncated (while writing)")
        # time2 = time.time()
        # print("write delay: %dus" %((time2-time1)*1e6))
