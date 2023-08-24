import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

import numpy as np

class HandLandmarkDetection:
    def __init__(self) -> None:
        model_file = open('models/hand_landmark_detection/hand_landmarker.task', "rb")
        model_data = model_file.read()
        model_file.close()

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
            # model_asset_path='models/hand_landmark_detection/hand_landmarker.task'),
            model_asset_buffer=model_data),
            num_hands=1,
            min_hand_detection_confidence=0.1,
            min_hand_presence_confidence=0.1,
            min_tracking_confidence=0.1,
            )
        self.detector = HandLandmarker.create_from_options(options)

        self.image = None
        self.landmarks = None
        self.position = None

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

    def run(self, frame):
        self.image = frame
        frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.detector.detect(frame)

        if len(detection_result.hand_landmarks) > 0:
            frame = self.draw_landmarks_on_image(
                frame.numpy_view(), detection_result
            )

            self.image = frame
            self.landmarks = detection_result.hand_landmarks[0]
