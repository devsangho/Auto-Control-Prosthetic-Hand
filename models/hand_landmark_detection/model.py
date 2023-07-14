import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


class HandLandmarkDetection:
    def __init__(self, cap) -> None:
        base_options = python.BaseOptions(
            model_asset_path="models/hand_landmark_detection/hand_landmarker.task",
        )
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.1,
            min_hand_presence_confidence=0.1,
            min_tracking_confidence=0.1,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.position = None
        self.cap = cap
        self.image = None
        self.detection_result = None

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in hand_landmarks
                ]
            )
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style(),
            )
        return annotated_image

    def run(self):
        print("GestureRecognizer running...")
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                continue
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            detection_result = self.detector.detect(image)

            annotated_image = self.draw_landmarks_on_image(
                image.numpy_view(), detection_result
            )

            self.detection_result = detection_result
            self.image = annotated_image

            print('detection_result: ', detection_result)
