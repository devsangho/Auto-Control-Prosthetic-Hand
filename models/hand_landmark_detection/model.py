import mediapipe as mp
import cv2


class HandLandmarkDetection:
    def __init__(self) -> None:
        self.image = None
        self.landmarks = None
        self.position = None

    def run(self, frame):
        self.image = frame
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(
                            color=(255, 0, 255), thickness=5, circle_radius=10
                        ),
                        mp_drawing.DrawingSpec(
                            color=(0, 255, 255), thickness=5, circle_radius=10
                        ),
                    )
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, _ = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        if id == 9:
                            cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

                    self.image = image
                self.landmarks = results.multi_hand_landmarks[0]
