#include <Servo.h>

Servo servo;

constexpr uint8_t motorAPins[] = {9, 11, 24, 26, 29, 31};
constexpr uint8_t motorBPins[] = {10, 12, 25, 27, 30, 32};
constexpr uint8_t enablePins[] = {2, 3, 4, 5, 6, 7};
constexpr uint8_t wiperPins[] = {A0, A1, A2, A3, A4, A5};
constexpr uint8_t servoPin = 33;

uint16_t pos[6];
uint8_t servo_pos = 0;

void setup() {
  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
    pinMode(motorAPins[thisMotor], OUTPUT);
    pinMode(motorBPins[thisMotor], OUTPUT);
    pinMode(enablePins[thisMotor], OUTPUT);
  }
  servo.attach(servoPin);
  Serial.begin(115200);

  servo.write(servo_pos);
}

void loop() {

  for(int thisMotor = 0; thisMotor < 6; thisMotor ++) {
    pos[thisMotor] = analogRead(wiperPins[thisMotor]);
    Serial.print(pos[thisMotor]);
    Serial.print("\t");
  }
  Serial.print(servo_pos);
  Serial.println("");
  delay(100);

  char temp[100];
  if(Serial.available()) {
    byte leng = Serial.readBytes(temp, 20);
    // Serial.print("Input data Lenght : ");
    // Serial.println(leng);
    // for(int i = 0; i < leng; i++){
    //   Serial.print(temp[i]);
    // }

    if(temp[0] == 'q' && leng == 2) {
      motorMove(1, 0, 200);
      delay(100);
      motorMove(3, 0, 200);
    }
    else if(temp[0] == 'w' && leng == 2) {
      motorMove(1, 1, 200);
      delay(100);
      motorMove(3, 1, 200);
    }
    else if(temp[0] == 'e' && leng == 2) {
      motorMove(1, 2, 200);
      delay(100);
      motorMove(3, 2, 200);
    }
    else if(temp[0] == 'r' && leng == 2) {
      motorMove(1, 3, 200);
      delay(100);
      motorMove(3, 3, 200);
    }
    else if(temp[0] == 't' && leng == 2) {
      motorMove(1, 4, 200);
      delay(100);
      motorMove(3, 4, 200);
    }
    else if(temp[0] == 'y' && leng == 2) {
      motorMove(1, 5, 200);
      delay(100);
      motorMove(3, 5, 200);
    }

    else if(temp[0] == 'a' && leng == 2) {
      motorMove(2, 0, 200);
      delay(100);
      motorMove(3, 0, 200);
    }
    else if(temp[0] == 's' && leng == 2) {
      motorMove(2, 1, 200);
      delay(100);
      motorMove(3, 1, 200);
    }
    else if(temp[0] == 'd' && leng == 2) {
      motorMove(2, 2, 200);
      delay(100);
      motorMove(3, 2, 200);
    }
    else if(temp[0] == 'f' && leng == 2) {
      motorMove(2, 3, 200);
      delay(100);
      motorMove(3, 3, 200);
    }
    else if(temp[0] == 'g' && leng == 2) {
      motorMove(2, 4, 200);
      delay(100);
      motorMove(3, 4, 200);
    }
    else if(temp[0] == 'h' && leng == 2) {
      motorMove(2, 5, 200);
      delay(100);
      motorMove(3, 5, 200);
    }

    else if(temp[0] == 'u' && leng == 2) {
      servo_pos += 10;
      servo.write(servo_pos);
    }
    else if(temp[0] == 'j' && leng == 2) {
      servo_pos -= 10;
      servo.write(servo_pos);
    }
  }

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
