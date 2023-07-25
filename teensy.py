import serial
import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
print([port.name for port in ports])

# 컴퓨터와 OS에 따라 serial_port는 달라질 수 있음.
# serial_port = '/dev/cu.usbmodem134065601'
serial_port1 = "/dev/cu.usbmodem134063301"
serial_port2 = "/dev/cu.usbmodem134114301"
serial_baudrate = 115200
time_out = 2
arduino1 = serial.Serial(port=serial_port1, baudrate=serial_baudrate, timeout=time_out)
arduino2 = serial.Serial(port=serial_port2, baudrate=serial_baudrate, timeout=time_out)


def sendToTeensy1(message):
    arduino1.write("/".encode() + str(message).encode())


def sendToTeensy2(message):
    arduino2.write("/".encode() + str(message).encode())
