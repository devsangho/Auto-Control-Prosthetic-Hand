import cv2
import numpy as np

raw_image = cv2.imread("../data/0000.jpg")
translated_image = None

imu_rotation_matrices = np.load("../data/labels.npy")
imu_rotation_matrix = imu_rotation_matrices[0]
imu_rotation_matrix = imu_rotation_matrix / imu_rotation_matrix[2][2]

print(imu_rotation_matrix)

translated_image = cv2.warpPerspective(raw_image, imu_rotation_matrix, (raw_image.shape[1], raw_image.shape[0]))

winname = "perspective transform"
display_width = 16 * 50
display_height = 9 * 50

cv2.namedWindow(winname)
cv2.resizeWindow(winname=winname, width=display_width * 2, height=display_height)
cv2.moveWindow(winname=winname, x=0, y=0)

horizontal_frames = np.hstack(
    [raw_image, translated_image]
)
horizontal_frames = cv2.resize(
    horizontal_frames,
    (display_width * 2, display_height),
    interpolation=cv2.INTER_AREA,
)
cv2.imshow(winname, horizontal_frames)

keycode = cv2.waitKey() & 0xFF
cv2.destroyAllWindows()