# Control of Prosthetic Hand with 6D Pose Estimation

## Motivation
When gripping an object, the axial rotation responsible for internal and external electrical conduction is the most important of the three degrees of freedom of the wrist. This is because, if it is impossible to rotate, it can be compensated by other movements of the arm and body, causing pain, discomfort, and secondary osteomyuscular diseases.

However, conventional prosthetic limbs have inconveniences in controlling the wrist or hand. Because you have to operate your wrist or hand one at a time using a dual control method that controls things with the same muscle.

![figure](https://github.com/devsangho/Control-of-Prosthetic-Hand-with-6D-Pose-Estimation/assets/54205862/092b7b99-e2e1-4cc4-ae08-b5aaf53f8941)

---

In this project, we conduct a study to control the rotation of the prosthetic wrist in consideration of the object's Pose and its surroundings.

1. **Adjust the angle of the prosthetic hand's wrist to the tilt of the object using images obtained from the human viewing angle.**
2. **It determines the situation in which the goods are handed over and controls them to respond flexibly.**

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
