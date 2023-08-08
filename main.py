import torch
import cv2
from worker import Worker
from models.objectron.model import Objectron
from models.hand_landmark_detection.model import HandLandmarkDetection
import numpy as np

from teensy import arduino1, arduino2
from processings import hand, angle
from sensors.imu import IMU

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    objectron = Objectron("Cup", cap)
    objectron_thread = Worker(name="objectron", model=objectron)

    hand_landmark_detection = HandLandmarkDetection(cap)
    hand_landmark_detection_thread = Worker(
        name="hand_landmark_detection", model=hand_landmark_detection
    )

    imu = IMU()
    imu_thread = Worker(name="imu", model=imu)

    arduino1_thread = Worker(name="arduino1", model=arduino1)
    arduino2_thread = Worker(name="arduino2", model=arduino2)

    arduino1_thread.start()
    arduino2_thread.start()
    objectron_thread.start()
    hand_landmark_detection_thread.start()
    imu_thread.start()

    with torch.no_grad():
        while cap.isOpened():
            if objectron.image is None or hand_landmark_detection.image is None:
                continue

            head_angle = None
            hand_position = hand.get_position(
                hand_landmark_detection.landmarks, objectron.landmarks_3d
            )

            # print(np.transpose(objectron.rotation_matrix), time.time())
            if (
                objectron.rotation_matrix is not None
                and imu.rotation_matrix is not None
            ):
                head_angle = angle.get_head_angle(
                    objectron.rotation_matrix, imu.rotation_matrix
                )
            # if head_angle is not None and objectron.landmarks_3d is not None:
            #     hand_angle = angle.get_hand_angle(head_angle)
            #     arduino2.send(hand_angle)

            # arduino2.send(hand_position)

            horizontal_images = np.hstack(
                [objectron.image, hand_landmark_detection.image]
            )

            text = "angle: " + str(head_angle) if head_angle is not None else "loading..."
            x, y, w, h = 0, 0, 700, 75
            cv2.rectangle(horizontal_images, (x, x), (x + w, y + h), (0, 0, 0), -1)
            cv2.putText(
                horizontal_images,
                text,
                (x + int(w / 10), y + int(h / 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            cv2.imshow("auto-prothetic-hand control system", horizontal_images)

            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
