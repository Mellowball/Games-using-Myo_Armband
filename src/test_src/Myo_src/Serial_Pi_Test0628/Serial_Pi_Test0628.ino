#include <SoftwareSerial.h>
String message = "";

SoftwareSerial testSerial(2, 3);
void setup() {
  Serial.begin(115200);
  testSerial.begin(115200);
//  pinMode(5, OUTPUT); 몇볼트 나오는지 테스트
}

void loop() {
  int ran = random(1,5);
  Serial.print("[");
  Serial.print(ran);
  Serial.print("]");
  delay(1000);
  // ---------------------------------------------------
//  Serial.println("test");
////  digitalWrite(5, HIGH); 몇볼트 나오는지 테스트
//  while (Serial.available()) {
//    message += (char)Serial.read();
//  }
//
//  if (message != 0) {
//    Serial.print(message);
//    message = "";
//  }
//  delay(200);
// ---------------------------------------------------
  //  while(testSerial.available()){
  //    message +=(char)testSerial.read();
  //    Serial.println("메시지 가는중");
  //  }
  //
  //  if(message != 0){
  //    testSerial.print(message);
  //    message = "";
  //  }
  //   delay(50);
  
} //loop
