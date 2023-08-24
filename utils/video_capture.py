import cv2
import threading, time


# Bufferless VideoCapture
# DO NOT USE without time.sleep(1/self.FPS) (massive frame loss)
# https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv
class VideoCapture:
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        self.FPS = 30
        self.lock = threading.Lock()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # Grab frames as soon as they are available
    def _reader(self):
        while True:
            with self.lock:
                ret = self.cap.grab()
            if not ret:
                print("Can't grab frame (stream end?). Exiting ...")
                break
            # Prevent cap.grab() from running to fast
            time.sleep(1/self.FPS)

    # Retrieve latest frame
    # if processing time is to short, Retrive last frame again
    # then total loop time is up to frame decodeing time (~15ms for 720p)
    def retrive(self):
        with self.lock:
            ret, frame = self.cap.retrieve()
        return ret, frame
    
    def isOpened(self):
        return self.cap.isOpened()
    
    def get(self, propid):
        return self.cap.get(propid)
    
    def release(self):
        self.cap.release()