import cv2
import mediapipe as mp
import numpy as np


class Objectron:
    def __init__(self, model_name) -> None:
        self.objectron = mp.solutions.objectron.Objectron(
            static_image_mode=False,
            max_num_objects=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.99,
            model_name=model_name,
        )
        self.image = None
        self.landmarks_3d = None
        self.rotation_matrix = None

    def run(self, frame):
        self.image = frame
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detection_result = self.objectron.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if detection_result.detected_objects:
            for detected_object in detection_result.detected_objects:
                landmarks = []
                for landmark in detected_object.landmarks_3d.landmark:
                    landmarks.append(landmark)

                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    detected_object.landmarks_2d,
                    mp.solutions.objectron.BOX_CONNECTIONS,
                )
                mp.solutions.drawing_utils.draw_axis(
                    frame, detected_object.rotation, detected_object.translation
                )

                self.image = frame
                self.landmarks_3d = landmarks
                self.rotation_matrix = np.array(detected_object.rotation)
        else:
            self.landmarks_3d = None
            self.rotation_matrix = None
