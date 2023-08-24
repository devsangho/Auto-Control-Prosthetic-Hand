import torch
import cv2
import numpy as np

from utils.serial_reader import Serial
from utils.video_capture import VideoCapture

from models.objectron.model import Objectron
from models.hand_landmark_detection.model import HandLandmarkDetection
from sensors.imu_and_emg import IMUAndEMG
from models.grasp_detection.model import GraspDetection

from processings import hand, angle
from config.teensy import serial_port1, serial_port2, serial_baudrate, timeout

import time


if __name__ == "__main__":
    ##################################################
    ##                Communication                 ##
    ##################################################
    serial_imu_emg = Serial(serial_port1, is_reading=True)
    serial_hand = Serial(serial_port2, is_reading=False)

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
    winname = 'auto-control-prosthetic-hand system'
    display_width = 16*50
    display_height = 9*50
    cv2.namedWindow(winname)
    cv2.resizeWindow(winname=winname, width=display_width*2, height=display_height)
    cv2.moveWindow(winname=winname, x=0, y=0)

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
            write_buffer_str = ''

            if objectron.rotation_matrix is not None and hand_landmark_detection.landmarks is not None:
                hand_position = hand.get_position(
                    hand_landmark_detection.landmarks, objectron.landmarks_3d
                )
                write_buffer_str += hand_position
            
            elif objectron.rotation_matrix is not None and imu_and_emg.rotation_matrix is not None:
                head_angle = angle.get_head_angle(
                    objectron.rotation_matrix, imu_and_emg.rotation_matrix
                )
                hand_angle = angle.get_hand_angle(head_angle)
                write_buffer_str += ("/%03d" %(hand_angle))


            if grasp_detection.y_pred is not None:
                if int(grasp_detection.y_pred) == 0:
                    pass
                elif int(grasp_detection.y_pred) == 1:
                    write_buffer_str += "grasp"
                    pass
                elif int(grasp_detection.y_pred) == 2:
                    write_buffer_str += "release"
                    pass

            if write_buffer_str != '':
                serial_hand.write(write_buffer_str)

            ##################################################
            ##                     GUI                      ##
            ##################################################
            # Add serial oscilloscope?

            horizontal_frames = np.hstack(
                [objectron.image, hand_landmark_detection.image]
            )
            horizontal_frames = cv2.resize(horizontal_frames, (display_width*2,display_height), interpolation = cv2.INTER_AREA)
            
            is_grasping = grasp_detection.y_pred
            text = (
                "is_grasping: " + str(is_grasping) if is_grasping is not None else "loading..."
            )
            w, h = 700, 50
            cv2.rectangle(
                img=horizontal_frames,
                pt1=(0,0),
                pt2=(w,h),
                color=(0, 0, 0),
                thickness=-1)
            cv2.putText(
                img=horizontal_frames,
                text=text,
                org=(int(w/50), int(h/1.5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=1,
            )
        
            cv2.imshow("auto-control-prosthetic-hand system", horizontal_frames)

            # cv2.pollKey()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            end_time = time.time()
            print("total loop: %dms" %((end_time-start_time)*1e3))

    cap.release()
    cv2.destroyAllWindows()
