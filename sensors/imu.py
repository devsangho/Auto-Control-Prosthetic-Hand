from teensy import arduino1


class IMU:
    def __init__(self):
        self.yaw, self.pitch, self.roll = None, None, None

    def run(self):
        print("IMU running...")
        arduino1.send("START_IMU")
        while arduino1.arduino.readable():
            raw_response = arduino1.arduino.readline()
            response = raw_response[0 : len(raw_response) - 1].decode().split("\t")

            if response[0] == "ypr":
                self.yaw, self.pitch, self.roll = (
                    float(response[1]),
                    float(response[2]),
                    float(response[3]),
                )
