from teensy import arduino1, arduino2

while True:
    command = input("command to arduino2: ")
    arduino2.arduino.write("/".encode() + str(command).encode())
