from teensy import arduino1, sendToTeensy1


class IMU:
    def __init__(self):
        self.yaw, self.pitch, self.roll = None, None, None

    def run(self):
        print("IMU running...")
        sendToTeensy1("START_IMU")
        while arduino1.readable():
            raw_response = arduino1.readline()
            response = raw_response[0 : len(raw_response) - 1].decode().split("\t")

            if response[0] == "ypr":
                self.yaw, self.pitch, self.roll = (
                    float(response[1]),
                    float(response[2]),
                    float(response[3]),
                )
