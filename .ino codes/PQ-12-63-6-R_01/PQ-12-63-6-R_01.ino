#include<Servo.h>

#define TIMER_INTERVAL 50
bool CALIBR = false;
uint8_t pos;
float control;
float cspeed = 0;
uint8_t init = 0;

Servo servo;

void servoControl(uint8_t target_pos, float speed) {
  if(target_pos > pos) {
    control = speed + cspeed;
    if(abs(control) < 1) {
      cspeed += speed;
    }
    else {
      cspeed = 0;
    }
  }
  else if(target_pos < pos) {
    control = - speed - cspeed;
    if(abs(control) < 1) {
      cspeed += speed;
    }
    else {
      cspeed = 0;
    }
  }
  else {
    control = 0;
  }

  if(pos != pos+int(control)) {servo.write(pos + int(control));}
  Serial.println(pos + int(control));
  pos = pos + int(control);
}

void setup() {
  Serial.begin(9600);

  if(CALIBR == false) {
    CALIBR = true;

    Serial.println("delay 2sec");
    delay(2000);
    Serial.println("delay end");

    Serial.println("init start");
    servo.write(init);
    pos = init;
    delay(3000);
    Serial.println("init end");
  }
}

void loop() {
  static int16_t timer = 0;
  uint32_t time = millis();
  static uint32_t pre_time = time - 1;
  uint16_t delta_time = time - pre_time;
  
  pre_time = time;
  timer -= delta_time;

  if(timer <= 0) {
    timer += TIMER_INTERVAL;
    
    //loop code
    servoControl(180, 1); //1~8정도
  }
}