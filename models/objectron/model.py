import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt


class Objectron:
    def __init__(self, model_name, cap) -> None:
        self.drawing = mp.solutions.drawing_utils
        self.objectron = mp.solutions.objectron.Objectron(
            static_image_mode=False,
            max_num_objects=5,
            min_detection_confidence=0.4,
            min_tracking_confidence=0.70,
            model_name=model_name,
        )
        self.cap = cap
        self.rotation_matrix = None
        self.image = None
        self.landmarks_3d = None

    def run(self):
        print("Objectron running...")
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                continue
            self.image = image
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = self.objectron.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if result.detected_objects:
                for detected_object in result.detected_objects:
                    landmarks = []
                    for landmark in detected_object.landmarks_3d.landmark:
                        landmarks.append(landmark)

                    self.rotation_matrix = np.array(detected_object.rotation)

                    self.drawing.draw_landmarks(
                        image,
                        detected_object.landmarks_2d,
                        mp.solutions.objectron.BOX_CONNECTIONS,
                    )
                    self.drawing.draw_axis(
                        image, detected_object.rotation, detected_object.translation
                    )

                    self.image = image
                    self.landmarks_3d = landmarks
