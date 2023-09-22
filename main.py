import torch
import cv2
import numpy as np

from utils.serial_reader import Serial
from utils.video_capture import VideoCapture
from utils.draw_axis import imu_draw_axis, objectron_draw_axis

from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from models.objectron.model import Objectron
from models.hand_landmark_detection.model import HandLandmarkDetection
from sensors.imu_and_emg import IMUAndEMG
from models.grasp_detection.model import GraspDetection

from processings import hand, angle
from config.teensy import serial_port1, serial_port2, serial_baudrate, timeout

import time

from queue import Queue
from scipy.ndimage import gaussian_filter1d

import pandas as pd


if __name__ == "__main__":
    ##################################################
    ##                Communication                 ##
    ##################################################
    serial_imu_emg = Serial(serial_port1, is_reading=True)
    # serial_hand = Serial(serial_port2, is_reading=False)

    cap = VideoCapture(0)
    # cap = cv2.VideoCapture(0)

    # check VideoCaptureAPI
    # 1400 MSMF (Microsoft Media Foundation)
    print(cap.get(cv2.CAP_PROP_BACKEND))
    # check camera FPS(not real FPS)
    print(cap.get(cv2.CAP_PROP_FPS))

    ##################################################
    ##                    Model                     ##
    ##################################################
    objectron = Objectron("Cup")
    hand_landmark_detection = HandLandmarkDetection()

    imu_and_emg = IMUAndEMG()

    grasp_detection = GraspDetection(
        emglist_ch1=imu_and_emg.emglist_ch1,
        emglist_ch2=imu_and_emg.emglist_ch2,
    )

    ##################################################
    ##                     GUI                      ##
    ##################################################
    winname = "auto-control-prosthetic-hand system"
    display_width = 16 * 50
    display_height = 9 * 50
    display_addon = 200

    cv2.namedWindow(winname)
    cv2.resizeWindow(winname=winname, width=display_width * 2, height=display_height+display_addon)
    cv2.moveWindow(winname=winname, x=0, y=0)

    serial_imu_emg.write("start!")

    angles_max_length = 200
    angles = []
    hand_angle = None
    estimated_angle = None
    hand_position = None

    with torch.no_grad():
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # task 1(500Hz)
            # read imu & emg data

            # task 2(~100ms loop)
            # capture frame > apply model > write calculated data

            start_time = time.time()
            ##################################################
            ##                Capture frame                 ##
            ##################################################
            # Capture frame-by-frame
            ret, frame = cap.retrive()

            # # Wait until next frame and Grab
            # # if processing time is over real camera FPS, becomes zero
            # cap.grab()
            # # Decode grabbed frame
            # ret, frame = cap.retrieve()

            # if frame is read correctly ret is True
            if not ret:
                # print("Can't receive frame (stream end?). Exiting ...")
                print("Can't retrive frame (stream end?). Exiting ...")
                break

            ##################################################
            ##                  Processing                  ##
            ##################################################
            imu_and_emg.buffer_to_data(serial_imu_emg.buffer_str)

            objectron.run(frame)
            hand_landmark_detection.run(frame)
            grasp_detection.run()

            head_angle = None
            write_buffer_str = ""

            hand_position = hand.get_position(
                hand_landmark_detection.landmarks, objectron.landmarks_3d
            )
            write_buffer_str += hand_position

            if (
                objectron.rotation_matrix is not None
                and imu_and_emg.rotation_matrix is not None
            ):
                head_angle = angle.get_head_angle(
                    objectron.rotation_matrix, imu_and_emg.rotation_matrix
                )
                hand_angle = angle.get_hand_angle(head_angle)
                angles.append(hand_angle)

            if grasp_detection.y_pred is not None:
                if int(grasp_detection.y_pred) == 0:
                    pass
                elif int(grasp_detection.y_pred) == 1:
                    write_buffer_str += "grasp"
                    pass
                elif int(grasp_detection.y_pred) == 2:
                    write_buffer_str += "release"
                    pass

            if len(angles) >= 1:
                estimated_angle = gaussian_filter1d(angles, sigma=20)[-1]
                write_buffer_str += "/%03d" % (estimated_angle)

            if write_buffer_str != "":
                # serial_hand.write(write_buffer_str)
                pass

            ##################################################
            ##                     GUI                      ##
            ##################################################
            # Add serial oscilloscope?

            horizontal_frames = np.hstack(
                [objectron.image, hand_landmark_detection.image]
            )
            horizontal_frames = cv2.resize(
                horizontal_frames,
                (display_width * 2, display_height),
                interpolation=cv2.INTER_AREA,
            )

            # objectron.rotation_matrix
            # imu_and_emg.rotation_matrix
            imu_axis_frame = np.zeros((display_addon, display_addon, 3), dtype=np.uint8)
            if imu_and_emg.rotation_matrix is not None:
                imu_rotation_matrix = imu_and_emg.rotation_matrix
                imu_axis_frame = imu_draw_axis(imu_axis_frame, imu_rotation_matrix)

            objectron_axis_frame = np.zeros((display_addon, display_addon, 3), dtype=np.uint8)
            if objectron.rotation_matrix is not None:
                objectron_rotation_matrix = np.array([[1,0,0],
                                                      [0,1,0],
                                                      [0,0,1],])
                objectron_rotation_matrix = np.matmul(objectron_rotation_matrix, objectron.rotation_matrix)
                objectron_rotation_matrix = np.matmul(objectron_rotation_matrix, objectron.rotation_matrix)
                objectron_axis_frame = objectron_draw_axis(objectron_axis_frame, objectron_rotation_matrix)

                # identity_rotation = R.identity()
                # objectron_rotation = R.from_matrix(objectron.rotation_matrix)

                # squared_objectron_rotaion = objectron_rotation * objectron_rotation
                # rotations = R.concatenate([identity_rotation, squared_objectron_rotaion])
                # key_times = [0, 2]
                # slerp = Slerp(key_times, rotations)
                # interpolated_rotation = slerp(1)

                # objectron_axis_frame = objectron_draw_axis(objectron_axis_frame, interpolated_rotation.as_matrix())

            object_axis_frame = np.zeros((display_addon, display_addon, 3), dtype=np.uint8)
            if imu_and_emg.rotation_matrix is not None and objectron.rotation_matrix is not None:
                axis_rotation_matrix = np.array([[0,0,-1],
                                                 [-1,0,0],
                                                 [0,1,0],])
                object_rotation_matrix = np.matmul(imu_and_emg.rotation_matrix, axis_rotation_matrix)
                object_rotation_matrix = np.matmul(object_rotation_matrix, objectron.rotation_matrix)
                object_rotation_matrix = np.matmul(object_rotation_matrix, objectron.rotation_matrix)
                object_rotation_matrix = np.matmul(object_rotation_matrix, axis_rotation_matrix.T)

                object_axis_frame = imu_draw_axis(object_axis_frame, object_rotation_matrix)

                # imu_rotation = R.from_matrix(imu_and_emg.rotation_matrix)
                # axis_rotation_matrix = np.array([[0,0,-1],
                #                                  [-1,0,0],
                #                                  [0,1,0],])
                # axis_rotation = R.from_matrix(axis_rotation_matrix)
                # identity_rotation = R.identity()
                # objectron_rotation = R.from_matrix(objectron.rotation_matrix)

                # squared_objectron_rotaion = objectron_rotation * objectron_rotation
                # rotations = R.concatenate([identity_rotation, squared_objectron_rotaion])
                # key_times = [0, 2]
                # slerp = Slerp(key_times, rotations)
                # interpolated_rotation = slerp(1)

                # object_rotation = imu_rotation * axis_rotation * interpolated_rotation * axis_rotation.inv()

                # object_axis_frame = imu_draw_axis(object_axis_frame, object_rotation.as_matrix())

            empty_frame = np.zeros((display_addon, display_width * 2 - (display_addon * 3), 3), dtype=np.uint8)

            axis_frame = np.hstack(
                [imu_axis_frame, objectron_axis_frame, object_axis_frame, empty_frame]
            )
            horizontal_frames = np.vstack(
                [horizontal_frames, axis_frame]
            )

            is_grasping = grasp_detection.y_pred
            text = (
                "is_grasping: " + str(is_grasping) + "   "
                if is_grasping is not None
                else "is_grasping: loading...   "
            )
            text = (
                text + "hand_angle: " + str(hand_angle) + "   "
                if hand_angle is not None
                else text + "hand_angle: loading...   "
            )
            text = (
                text + "hand position: " + str(hand_position)
                if hand_position is not None
                else text + "hand_position: loading..."
            )
            w, h = 2000, 50
            cv2.rectangle(
                img=horizontal_frames,
                pt1=(0, 0),
                pt2=(w, h),
                color=(0, 0, 0),
                thickness=-1,
            )
            cv2.putText(
                img=horizontal_frames,
                text=text,
                org=(int(w / 50), int(h / 1.5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=1,
            )

            cv2.imshow("auto-control-prosthetic-hand system", horizontal_frames)

            # cv2.pollKey()
            if cv2.waitKey(1) & 0xFF == ord("q"):
                # Save csv file
                # df = pd.DataFrame(angles, columns = ['hand_angles'])
                # df.to_csv("hand_angles.csv", index = False)
                break

            end_time = time.time()
            # print("total loop: %dms" % ((end_time - start_time) * 1e3))

    cap.release()
    cv2.destroyAllWindows()
