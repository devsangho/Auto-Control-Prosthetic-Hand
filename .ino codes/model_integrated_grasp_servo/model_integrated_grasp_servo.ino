#include <Servo.h>

Servo servo;

constexpr uint8_t motorAPins[] = {9, 11, 24, 26, 29, 31};
constexpr uint8_t motorBPins[] = {10, 12, 25, 27, 30, 32};
constexpr uint8_t enablePins[] = {2, 3, 4, 5, 6, 7};
constexpr uint8_t wiperPins[] = {A0, A1, A2, A3, A4, A5};
constexpr uint8_t servoPin = 33;

int pos[7];
int temp[7];

int min_pos[7] = {30, 30, 50, 50, 50, 50, 0};
int max_pos[7] = {950, 250, 650, 650, 650, 650, 180};
//1 motor min: 0, max: 950
//2 motor min: 0, max: 250
//3~6 motor min: 50, max: 650
//servo motor min: 0, max: 180
int grasp_pos[7] = {720, 30, 361, 355, 308, 344};
//1 motor 720
//2 motor 16
//3 motor 361
//4 motor 355
//5 motor 308
//6 motor 344

void setup() {
  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
    pinMode(motorAPins[thisMotor], OUTPUT);
    pinMode(motorBPins[thisMotor], OUTPUT);
    pinMode(enablePins[thisMotor], OUTPUT);
  }
  servo.attach(servoPin);
  Serial.begin(115200);

  pos[6] = 0;
  servo.write(pos[6]);
}

void loop() {
  ////////////////////////////////////////////////////////////////////////////////////////////////////
  //serial input
  char buffer[10];
  if(Serial.available()) {
    byte leng = Serial.readBytesUntil('\n', buffer, 20);
    // Serial.print("Input data Lenght : ");
    // Serial.println(leng);
    // for(int i = 0; i < leng; i ++){
    //   Serial.print(buffer[i]);
    // }
    // Serial.println("");

    String str = String(buffer);
    // Serial.println(str);

    if(str.indexOf('q') != -1) {
      temp[0] += 10;
    }
    if(str.indexOf('w') != -1) {
      temp[1] += 10;
    }
    if(str.indexOf('e') != -1) {
      temp[2] += 10;
    }
    if(str.indexOf('r') != -1) {
      temp[3] += 10;
    }
    if(str.indexOf('t') != -1) {
      temp[4] += 10;
    }
    if(str.indexOf('y') != -1) {
      temp[5] += 10;
    }
    if(str.indexOf('u') != -1) {
      temp[6] += 10;
    }

    if(str.indexOf('a') != -1) {
      temp[0] -= 10;
    }
    if(str.indexOf('s') != -1) {
      temp[1] -= 10;
    }
    if(str.indexOf('d') != -1) {
      temp[2] -= 10;
    }
    if(str.indexOf('f') != -1) {
      temp[3] -= 10;
    }
    if(str.indexOf('g') != -1) {
      temp[4] -= 10;
    }
    if(str.indexOf('h') != -1) {
      temp[5] -= 10;
    }
    if(str.indexOf('j') != -1) {
      temp[6] -= 10;
    }

    if(str.indexOf('z') != -1) {
      extractionRetraction(1);
    }
    else if(str.indexOf('x') != -1) {
      extractionRetraction(2);
    }

    if(str.lastIndexOf('/') != -1) {
      int angle_index = str.lastIndexOf('/') + 1;
      int angle = str.substring(angle_index).toInt();
      wristMove(angle);
    }
  }
  // for(int thisMotor = 0; thisMotor < 7; thisMotor ++){
  //   Serial.print(temp[thisMotor]);
  //   Serial.print("\t");
  // }
  // Serial.println("");

  ////////////////////////////////////////////////////////////////////////////////////////////////////
  //serial output (error)
  // for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
  //   pos[thisMotor] = analogRead(wiperPins[thisMotor]);
  //   Serial.print(pos[thisMotor]);
  //   Serial.print("\t");
  // }
  // Serial.print(pos[6]);
  // Serial.println("");

  ////////////////////////////////////////////////////////////////////////////////////////////////////
  //motor control
  //1 motor min: 0, max: 950
  if(temp[0] > 0 && pos[0] < max_pos[0]) {
    motorMove(1, 0, 200);
    temp[0] -= 1;
  }
  else if(temp[0] < 0 && pos[0] > min_pos[0]) {
    motorMove(2, 0, 200);
    temp[0] += 1;
  }
  else {
    motorMove(3, 0, 200);
    temp[0] = 0;
  }
  //2 motor min: 0, max: 250
  if(temp[1] > 0 && pos[1] < max_pos[1]) {
    motorMove(1, 1, 200);
    temp[1] -= 1;
  }
  else if(temp[1] < 0 && pos[1] > min_pos[1]) {
    motorMove(2, 1, 200);
    temp[1] += 1;
  }
  else {
    motorMove(3, 1, 200);
    temp[1] = 0;
  }
  //3~6 motor min: 50, max: 650
  for(int thisMotor = 2; thisMotor < 6; thisMotor ++) {
    if(temp[thisMotor] > 0 && pos[thisMotor] < max_pos[thisMotor]) {
      motorMove(1, thisMotor, 200);
      temp[thisMotor] -= 1;
    }
    else if(temp[thisMotor] < 0 && pos[thisMotor] > min_pos[thisMotor]) {
      motorMove(2, thisMotor, 200);
      temp[thisMotor] += 1;
    }
    else {
      motorMove(3, thisMotor, 200);
      temp[thisMotor] = 0;
    }
  }
  //servo motor min: 0, max: 180
  if(temp[6] > 0) {
    temp[6] -= 1;
    if(pos[6] < max_pos[6]) {
      pos[6] += 1;
      servo.write(pos[6]);
    }
    else {
      temp[6] = 0;
    }
  }
  else if(temp[6] < 0) {
    temp[6] += 1;
    if(pos[6] > min_pos[6]) {
      pos[6] -= 1;
      servo.write(pos[6]);
    }
    else {
      temp[6] = 0;
    }
  }
  delay(10);

}

void motorMove(int type, int thisMotor, int pwm) {
  //1(forward), 2(backward), 3(stop)

  analogWrite(enablePins[thisMotor], pwm);
    switch(type) {
      case 1:
        digitalWrite(motorAPins[thisMotor],HIGH);
        digitalWrite(motorBPins[thisMotor],LOW);
        break;
      case 2:
        digitalWrite(motorAPins[thisMotor],LOW);
        digitalWrite(motorBPins[thisMotor],HIGH);
        break;
      case 3:
        digitalWrite(motorAPins[thisMotor],HIGH);
        digitalWrite(motorBPins[thisMotor],HIGH);
        break;
  }
}

void extractionRetraction(int type) {
  //1(extraction), 2(retraction)
  switch(type) {
    case 1:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        temp[thisMotor] = max_pos[thisMotor] - pos[thisMotor];
      }
      break;
    case 2:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        temp[thisMotor] = min_pos[thisMotor] - pos[thisMotor];
      }
      break;
  }
}

void graspRelease(int type) {
  //1(grasp), 2(release)
  switch(type) {
    case 1:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        temp[thisMotor] = grasp_pos[thisMotor] - pos[thisMotor];
      }
      break;
    case 2:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        temp[thisMotor] = min_pos[thisMotor] - pos[thisMotor];
      }
      break;
  }
}

void wristMove(int angle) {
  temp[6] = angle - pos[6];
}