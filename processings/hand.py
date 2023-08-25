import numpy as np


def align_coordinate_to_camera_coordinate_2d_system(landmark):
    return {
        "x": 0.5 - landmark.x,
        "y": 0.5 - landmark.y,
    }


def get_position(hand_landmarks, object_landmarks) -> str:
    if hand_landmarks is None or hand_landmarks == []:
        return "NULL"
    if object_landmarks is None or object_landmarks == []:
        return "NULL"

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

    center_of_object = object_landmarks[0]
    center_of_hand = align_coordinate_to_camera_coordinate_2d_system(
        hand_landmarks.landmark[9]
    )

    if top_of_object < center_of_hand["y"]:
        return "up"
    if down_of_object > center_of_hand["y"]:
        return "down"
    if center_of_object.x < center_of_hand["x"]:
        return "left"
    if center_of_object.x > center_of_hand["x"]:
        return "right"
