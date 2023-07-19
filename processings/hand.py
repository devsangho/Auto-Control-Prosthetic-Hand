import numpy as np


def get_position(hand_landmarks, object_landmarks) -> str:
    if hand_landmarks is None or hand_landmarks == []:
        return "NULL"
    if object_landmarks is None or object_landmarks == []:
        return "NULL"

    print("object_landmarks[3]", len(object_landmarks))

    top_of_object = np.mean(
        [
            np.array(object_landmarks[3].y),
            np.array(object_landmarks[4].y),
            np.array(object_landmarks[8].y),
            np.array(object_landmarks[7].y),
        ],
        axis=0,
    )
    down_of_object = np.mean(
        [
            np.array(object_landmarks[1].y),
            np.array(object_landmarks[2].y),
            np.array(object_landmarks[6].y),
            np.array(object_landmarks[5].y),
        ],
        axis=0,
    )

    print("top_of_object", top_of_object, "down_of_object", down_of_object)
    center_of_object = object_landmarks[0]
    center_of_hand = hand_landmarks[0]

    if top_of_object < center_of_hand.y:
        return "UP"
    if down_of_object > center_of_hand.y:
        return "DOWN"
    if center_of_object.x < center_of_hand.x:
        return "RIGHT"
    if center_of_object.x > center_of_hand.x:
        return "LEFT"
