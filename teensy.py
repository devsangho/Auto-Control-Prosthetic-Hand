import serial
import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()

print([port.name for port in ports])

# 컴퓨터와 OS에 따라 serial_port는 달라질 수 있음.
serial_port = '/dev/cu.usbmodem134065601'
serial_baudrate = 9600
time_out = 2
arduino = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=time_out)

while True:
      
    commend = input('send to arduino : ')
    
    arduino.write(commend.encode())
    
    time.sleep(0.1)
    
    if arduino.readable():
        
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받는다.)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = arduino.readline()
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())