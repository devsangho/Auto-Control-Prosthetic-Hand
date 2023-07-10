import time
import cv2
import torch
import numpy as np

from numpy import random
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, check_requirements, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

import math

import mediapipe as mp

import cv2
import numpy as np
import matplotlib.pyplot as plt

from teensy import sendToTeensy, arduino


mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils


WEIGHTS = 'yolov7-tiny.pt'
IMG_SIZE = 640
DEVICE = ''
AUGMENT = False
CONF_THRES = 0.25
IOU_THRES = 0.45
CLASSES = None
AGNOSTIC_NMS = False

hide_conf=False
line_thickness=3


# Webcam
cap = cv2.VideoCapture(0)

# Initialize
device = select_device(DEVICE)
half = device.type != 'cpu'  # half precision only supported on CUDA
print('device:', device)

# Load yolo model
model = attempt_load(WEIGHTS, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride
imgsz = check_img_size(IMG_SIZE, s=stride)  # check img_size
if half:
    model.half()  # to FP16

# Load mediapipe objectron model
objectron_cup = mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=5,
                            min_detection_confidence=0.4,
                            min_tracking_confidence=0.70,
                            model_name='Cup')

# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

# Run inference
if device.type != 'cpu':
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once


def find_plane(points):
    c = np.mean(points, axis=0)
    r0 = points - c
    u, s, v = np.linalg.svd(r0)
    nv = v[-1, :]
    ds = np.dot(points, nv)
    param = np.r_[nv, -np.mean(ds)]
    return param

# Detect function
def detect(frame):
    # Load image
    img0 = frame

    # Padded resize
    img = letterbox(img0, imgsz, stride=stride)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)


    # Inference
    t0 = time_synchronized()
    pred = model(img, augment=AUGMENT)[0]

    # Apply NMS
    pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, classes=CLASSES, agnostic=AGNOSTIC_NMS)

    # Process detections
    det = pred[0]

    s = ''
    s += '%gx%g ' % img.shape[2:]  # print string

    if len(det):
        # Rescale boxes from img_size to img0 size
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

        # Print results
        for c in det[:, -1].unique():
            n = (det[:, -1] == c).sum()  # detections per class
            s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

        # Write results
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'
            plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=3)

        print(f'Inferencing and Processing Done. ({time.time() - t0:.3f}s)')

    # return results
    return img0

# Read video stream and feed into the model
check_requirements(exclude=('pycocotools', 'thop'))
with torch.no_grad():
    while cap.isOpened():
        ret, frame = cap.read()
        yolo_result = detect(frame)

        success, image = cap.read()

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = [objectron_cup.process(image)]

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        estimated_angle = 0
        for result in results:
            if result.detected_objects:
                for detected_object in result.detected_objects:
                    y_rotation = [detected_object.rotation[0][1], detected_object.rotation[1][1], detected_object.rotation[2][1]]
                    y_unitVector = np.array([0, 1, 0])
                    
                    inner_product = np.inner(y_rotation, y_unitVector)
                    norm_product = np.multiply(np.linalg.norm(y_rotation), np.linalg.norm(y_unitVector))

                    theta = np.arccos(np.divide(inner_product, norm_product)) * 180 / np.pi
                    estimated_angle = theta
                    
                    # mp_drawing.draw_landmarks(image, 
                    #                           detected_object.landmarks_2d, 
                    #                           mp_objectron.BOX_CONNECTIONS)
                    
                    mp_drawing.draw_axis(image, 
                                        detected_object.rotation,
                                        detected_object.translation)

            horizontal_images = np.hstack((image, yolo_result))
            sendToTeensy(estimated_angle)
            cv2.putText(horizontal_images, 'Estimated angle: ' + str(estimated_angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow('', horizontal_images)

            if arduino.readable():
                # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받는다.)
                # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
                response = arduino.readline()
                
                # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
                print(response[:len(response)-1].decode())
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()