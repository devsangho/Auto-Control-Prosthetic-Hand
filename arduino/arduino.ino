char cmd;

void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
}

void loop() {
  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if (Serial.available()) {
    cmd = Serial.read();
    Serial.println(cmd);
  }
}