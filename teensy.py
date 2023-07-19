import serial
import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
print([port.name for port in ports])

# 컴퓨터와 OS에 따라 serial_port는 달라질 수 있음.
# serial_port = '/dev/cu.usbmodem134065601'
serial_port = "COM3"
serial_baudrate = 115200
time_out = 2
arduino = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=time_out)


def sendToTeensy(message):
    arduino.write("/".encode() + str(message).encode())
