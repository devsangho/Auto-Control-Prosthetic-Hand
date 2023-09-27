# Control of Prosthetic Hand with 6D Pose Estimation

In this project, we conduct a study to control the rotation of the prosthetic wrist in consideration of the object's Pose and its surroundings.

1. Adjust the angle of the prosthetic hand's wrist to the tilt of the object using images obtained from the human viewing angle.

2. It determines the situation in which the goods are handed over and controls them to respond flexibly.

This project uses [Objectron](https://github.com/google/mediapipe/blob/master/docs/solutions/objectron.md), [Hand Landmakrs Detection Model](https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md) and eEMG Model to control prosthetic hand to pick up and receive objects.

## Demo
### 1. Adjust the angle of the prosthetic hand's wrist to the tilt of the object using images obtained from the human viewing angle.
![demo2](./docs/demo2.gif)

### 2. It determines the situation in which the goods are handed over and controls them to respond flexibly.

![demo1](./docs/demo1.gif)

[More Information](./docs/poster.pdf)

---

## Installation

```shell
pip install -r requirements.txt
```

## Run

```shell
python main.py
```

## Maintainers
- [Sangho Yoon](https://github.com/devsangho)
- [Seongbin Park](https://github.com/seuino)

## Team
- organized by [AIMS(AI For Mechanical System)](https://www.aims-cau.com/).
