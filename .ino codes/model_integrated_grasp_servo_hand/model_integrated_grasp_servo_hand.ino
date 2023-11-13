#include <Servo.h>

// #define INDIVIDUAL_CONTROL
// #define FULL_CONTROL
// #define GRASP_DETECTION_CONTROL

// #define DEFAULT_WRIST_CONTROL
// #define HAND_LANDMARK_DETECTION_WRIST_CONTROL

#define DISPLAY_MODE

// #define DEBUG_MODE

#define CONTROL_FREQUENCY 500

Servo servo;

constexpr uint8_t motorAPins[] = {9, 11, 24, 26, 29, 31};
constexpr uint8_t motorBPins[] = {10, 12, 25, 27, 30, 32};
constexpr uint8_t enablePins[] = {2, 3, 4, 5, 6, 7};
constexpr uint8_t wiperPins[] = {A0, A1, A2, A3, A4, A5};
constexpr uint8_t servoPin = 33;

int pos[7];
float temp[7];
uint8_t status[7] = {2, 2, 2, 2, 2, 2, 0};
//1 = extracting
//2 = retracting
//3 = resting
bool trigger = false;

int min_pos[7] = {50, 50, 80, 80, 90, 80, 0};
int max_pos[7] = {900, 400, 630, 630, 630, 630, 180};
int grasp_pos[7] = {648, 50, 382, 384, 432, 464};

unsigned long timeStamp;

void setup() {
  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
    pinMode(motorAPins[thisMotor], OUTPUT);
    pinMode(motorBPins[thisMotor], OUTPUT);
    pinMode(enablePins[thisMotor], OUTPUT);
  }
  servo.attach(servoPin);
  Serial.begin(115200);

  servo.write(0);
  pos[6] = 0;
}

void loop() {
  timeStamp = micros();
  //////////////////////////////////////////////////
  //                 Positioning                  //
  //////////////////////////////////////////////////
  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
    pos[thisMotor] = analogRead(wiperPins[thisMotor]);
  }

  //////////////////////////////////////////////////
  //                 Serial input                 //
  //////////////////////////////////////////////////
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

    #ifdef INDIVIDUAL_CONTROL
      // asdfghj
      if(str.indexOf('q') != -1) {temp[0] += 5;}
      if(str.indexOf('w') != -1) {temp[1] += 5;}
      if(str.indexOf('e') != -1) {temp[2] += 5;}
      if(str.indexOf('r') != -1) {temp[3] += 5;}
      if(str.indexOf('t') != -1) {temp[4] += 5;}
      if(str.indexOf('y') != -1) {temp[5] += 5;}
      if(str.indexOf('u') != -1) {temp[6] += 5;}
      // qwertyu
      if(str.indexOf('a') != -1) {temp[0] -= 5;}
      if(str.indexOf('s') != -1) {temp[1] -= 5;}
      if(str.indexOf('d') != -1) {temp[2] -= 5;}
      if(str.indexOf('f') != -1) {temp[3] -= 5;}
      if(str.indexOf('g') != -1) {temp[4] -= 5;}
      if(str.indexOf('h') != -1) {temp[5] -= 5;}
      if(str.indexOf('j') != -1) {temp[6] -= 5;}
    #endif

    #ifdef FULL_CONTROL
      // zx
      if(str.indexOf('z') != -1) {fullExtractionRetraction(1);}
      else if(str.indexOf('x') != -1) {fullExtractionRetraction(2);}
      // cv
      if(str.indexOf('c') != -1) {fullGraspRelease(1);}
      else if(str.indexOf('v') != -1) {fullGraspRelease(2);}
    #endif

    #ifdef GRASP_DETECTION_CONTROL
      if(str.indexOf("grasp") != -1) {gradualGraspRelease(1);}
      else if(str.indexOf("release") != -1) {gradualGraspRelease(2);}
    #endif

    // Control wrist angle
    #ifdef HAND_LANDMARK_DETECTION_WRIST_CONTROL
      #undef DEFAULT_WRIST_CONTROL
      // up, down, left, right priority
      if(str.indexOf("up") != -1) {wristMove(180);}
      else if(str.indexOf("down") != -1) {wristMove(0);}
      else if(str.indexOf("left") != -1) {wristMove(90);}
      // /{wrist_angle}
      else if(str.indexOf('/') != -1) {
        int angle_index = str.indexOf('/') + 1;
        int angle = str.substring(angle_index, angle_index+3).toInt();
        wristMove(angle);
      }
    #endif

    #ifdef DEFAULT_WRIST_CONTROL
      // /{wrist_angle}
      if(str.indexOf('/') != -1) {
        int angle_index = str.indexOf('/') + 1;
        int angle = str.substring(angle_index, angle_index+3).toInt();
        wristMove(angle);
      }
    #endif
  }

  #ifdef DISPLAY_MODE
    for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
      // Extract or retract or rest
      if(status[thisMotor] == 1) {
        temp[thisMotor] += 5;
        if(pos[thisMotor] >= max_pos[thisMotor]) {status[thisMotor] = 2;}
      }
      else if(status[thisMotor] == 2) {
        temp[thisMotor] -= 5;
        if(pos[thisMotor] <= min_pos[thisMotor]) {status[thisMotor] = 3;}
      }
      else if(status[thisMotor] == 3) {}
    }

    if(status[0] == 3 && status[1] == 3 && status[2] == 3 && status[3] == 3 &&\
    status[4] == 3 && status[5] == 3) {
      // for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
      //   status[thisMotor] = 1;
      // }
      trigger = true;
      status[0] = 1;
    }

    if(trigger) {
      if(pos[0] >= (max_pos[0] - min_pos[0])/12 + min_pos[0]) {status[1] = 1;}
      if(pos[1] >= (max_pos[1] - min_pos[1])/12*6 + min_pos[1]) {status[2] = 1;}
      if(pos[2] >= (max_pos[2] - min_pos[2])/12 + min_pos[2]) {status[3] = 1;}
      if(pos[3] >= (max_pos[3] - min_pos[3])/12 + min_pos[3]) {status[4] = 1;}
      if(pos[4] >= (max_pos[4] - min_pos[4])/12 + min_pos[4]) {status[5] = 1; trigger = false;}
    }
  #endif

  //////////////////////////////////////////////////
  //                Motor control                 //
  //////////////////////////////////////////////////
  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
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

  //////////////////////////////////////////////////
  //                Serial output                 //
  //////////////////////////////////////////////////
  delay(5);

  #ifdef DEBUG_MODE
    for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
      Serial.print(pos[thisMotor]);
      Serial.print("(");
      Serial.print(status[thisMotor]);
      Serial.print(")");
      Serial.print("\t");
    }
    Serial.print(pos[6]);
    Serial.print("\t");
    Serial.print((micros() - timeStamp)*1e-3);
    Serial.print("ms");
    Serial.println("");
  #endif
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

void gradualGraspRelease(int type) {
  //1(grasp), 2(release)
  switch(type) {
    case 1:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        int temp_gradual = grasp_pos[thisMotor] - pos[thisMotor];
        if(temp_gradual > 10) {
          temp_gradual = 10;
        }
        else if(temp_gradual < -10) {
          temp_gradual = -10;
        }
        temp[thisMotor] = temp_gradual;
      }
      break;
    case 2:
      for(int thisMotor = 0; thisMotor < 7; thisMotor ++) {
        int temp_gradual = min_pos[thisMotor] - pos[thisMotor];
        if(temp_gradual > 10) {
          temp_gradual = 10;
        }
        else if(temp_gradual < -10) {
          temp_gradual = -10;
        }
        temp[thisMotor] = temp_gradual;
      }
      break;
  }
}

void fullExtractionRetraction(int type) {
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

void fullGraspRelease(int type) {
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