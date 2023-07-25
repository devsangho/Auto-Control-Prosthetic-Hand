from teensy import arduino1, sendToTeensy1


class IMU:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.w = None

    def run(self):
        print("IMU running...")
        sendToTeensy1("START_IMU")
        while arduino1.readable():
            raw_response = arduino1.readline()
            response = raw_response[0 : len(raw_response) - 1].decode().split("\t")
            if response[0] == "quat":
                self.x = float(response[1])
                self.y = float(response[2])
                self.z = float(response[3])
                self.w = float(response[4])
