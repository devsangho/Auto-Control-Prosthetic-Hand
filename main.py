import torch
import cv2
from worker import Worker
from models.objectron.model import Objectron
from models.hand_landmark_detection.model import HandLandmarkDetection
import numpy as np

from teensy import arduino, sendToTeensy
from processings import hand

cap = cv2.VideoCapture(0)


if __name__ == "__main__":
    objectron = Objectron("Cup", cap)
    objectron_thread = Worker(name="objectron", model=objectron)

    hand_landmark_detection = HandLandmarkDetection(cap)
    hand_landmark_detection_thread = Worker(
        name="hand_landmark_detection", model=hand_landmark_detection
    )

    objectron_thread.start()
    hand_landmark_detection_thread.start()

    with torch.no_grad():
        while cap.isOpened():
            if objectron.image is None or hand_landmark_detection.image is None:
                continue

            hand_position = hand.get_position(
                hand_landmark_detection.landmarks, objectron.landmarks_3d
            )

            sendToTeensy(objectron.angle)
            sendToTeensy(hand_position)

            horizontal_images = np.hstack(
                [objectron.image, hand_landmark_detection.image]
            )

            cv2.imshow("auto-prothetic-hand control system", horizontal_images)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
