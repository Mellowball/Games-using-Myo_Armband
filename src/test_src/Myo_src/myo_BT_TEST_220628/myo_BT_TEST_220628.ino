
#include <MyoBridge.h>
#include <SoftwareSerial.h>
#include <MyoArduino.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

#define WAVEIN_PIN 8
#define WAVEOUT_PIN 7

#define LEFT_PIN 4
#define RIGHT_PIN 5

#define Piezo_PIN 10

int tones[] = {261, 294, 330, 349, 392, 440, 494, 523};

//SoftwareSerial connection to MyoBridge
SoftwareSerial bridgeSerial(2, 3); // TX RX
LiquidCrystal_I2C lcd(0x27, 20, 2); // 1번 0x27, 2번 0x3E set the LCD address to 0x27 for a 16 chars and 2 line display
//initialise MyoBridge object with software serial connection
MyoBridge bridge(bridgeSerial);

//declare a function to handle pose data
void handlePoseData(MyoPoseData& data) {

  //convert pose data to MyoPose
  MyoPose pose;
  pose = (MyoPose)data.pose;

  //assign a pose number
  Output output;
  int poseNum = output.poseNumber(bridge.poseToString(pose));
  //Serial.println(pose);
  //assign poses different actions
  //LED on pin 4 will be controlled by "Fist"
  //LED on pin 5 will be controlled by "Wave Out"
  //LED on pin 6 will be controlled by "Fingers Spread"

  switch (poseNum)
  {
    case 1:
      //      Serial.println("Resting");
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, HIGH);
      digitalWrite(LEFT_PIN, HIGH); // LED
      digitalWrite(RIGHT_PIN, HIGH);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Resting");
      Serial.print("[");
      Serial.print("1");
      Serial.println("]");
      delay(50);

      break;
    case 2:
      //      Serial.println("Fist");
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, HIGH);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("FIST");
      Serial.print("[");
      Serial.print("2");
      Serial.println("]");
      delay(50);
      break;

    case 3:
      //      Serial.println("Wave In");
      lcd.clear();
      digitalWrite(WAVEIN_PIN, LOW);
      digitalWrite(WAVEOUT_PIN, HIGH);
      digitalWrite(LEFT_PIN, LOW); // LED
      digitalWrite(RIGHT_PIN, HIGH);
      lcd.setCursor(0, 1);
      lcd.println("WAVE IN");
      Serial.print("[");
      Serial.print("3");
      Serial.println("]");
      delay(50);
      break;

    case 4:
      //      Serial.println("Wave Out");
      lcd.clear();
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, LOW);
      digitalWrite(LEFT_PIN, HIGH); // LED
      digitalWrite(RIGHT_PIN, LOW);
      lcd.setCursor(0, 1);
      lcd.print("WAVE OUT");
      Serial.print("[");
      Serial.print("4");
      Serial.println("]");
      delay(50);
      break;

    case 5:
      //      Serial.println("Fingers Spread 1");
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, HIGH);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("FingersSpread");
      //delay(500);
      Serial.print("[");
      Serial.print("5");
      Serial.println("]");
      delay(50);

      break;
    case 6:
      //      Serial.println("TAPTAP");
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, HIGH);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("DoubleTap");
      Serial.print("[");
      Serial.print("6");
      Serial.println("]");
      delay(50);

      break;
    //delay(300);
    default:
      //      Serial.println("Defalut");
      digitalWrite(WAVEIN_PIN, HIGH);
      digitalWrite(WAVEOUT_PIN, HIGH);
      digitalWrite(LEFT_PIN, LOW); // LED
      digitalWrite(RIGHT_PIN, LOW);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Defalut") ;
      delay(50);
      
      break;
  }// switch (poseNum)
}// handlePoseData(MyoPoseData& data)

void setup() {
  //initialise both serial connections

  Serial.begin(115200);
  Serial.println("Myo Armband");
  bridgeSerial.begin(115200);
  pinMode(WAVEIN_PIN, OUTPUT);
  pinMode(WAVEOUT_PIN, OUTPUT);

  pinMode(LEFT_PIN, OUTPUT);
  pinMode(RIGHT_PIN, OUTPUT);

  pinMode(Piezo_PIN, OUTPUT);

  lcd.init();                      // initialize the lcd
  lcd.backlight();
  lcd.setCursor(2, 0);
  lcd.print("Myo Armband");
  digitalWrite(WAVEIN_PIN, HIGH);
  digitalWrite(WAVEOUT_PIN, HIGH);

  digitalWrite(LEFT_PIN, HIGH); // LED
  digitalWrite(RIGHT_PIN, HIGH);
  delay(600);
  digitalWrite(LEFT_PIN, LOW); // LED
  digitalWrite(RIGHT_PIN, LOW);
  delay(600);
  digitalWrite(LEFT_PIN, HIGH); // LED
  digitalWrite(RIGHT_PIN, LOW);
  delay(600);
  digitalWrite(LEFT_PIN, LOW); // LED
  digitalWrite(RIGHT_PIN, HIGH);
  delay(600);
  digitalWrite(LEFT_PIN, LOW); // LED
  digitalWrite(RIGHT_PIN, LOW);
  delay(600);
  // digitalWrite(WAVEIN_PIN,HIGH);
  // digitalWrite(WAVEOUT_PIN,HIGH);
  tone(Piezo_PIN, tones[7]);
  delay(150);
  noTone(Piezo_PIN);
  delay(250);


  lcd.setCursor(0, 1);
  lcd.print("Initialization!!");
  delay(2000);
  lcd.clear();
  delay(800);

  lcd.setCursor(2, 0);
  lcd.print("Myo Armband");
  lcd.setCursor(0, 1);
  lcd.print("Initialization!!");
  delay(2000);
  lcd.clear();
  delay(800);

  //wait until MyoBridge has found Myo and is connected. Make sure Myo is not connected to anything else and not in standby!
  lcd.setCursor(2, 0);
  lcd.print("Searching for Myo...");
  Serial.println("Searching for Myo...");
  bridge.begin();
  lcd.setCursor(0, 1);
  lcd.print("connected!");
  Serial.println("connected!");
  delay(300);
  lcd.clear();

  tone(Piezo_PIN, tones[7]);
  delay(150);
  tone(Piezo_PIN, tones[7]);
  delay(150);
  noTone(Piezo_PIN);
  delay(250);

  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print("waiting for pose!");
  Serial.println("waiting for pose!");
  //set the function that handles pose events
  bridge.setPoseEventCallBack(handlePoseData);
  //tell the Myo we want Pose data
  bridge.enablePoseData();
  //make sure Myo is unlocked
  bridge.unlockMyo();
  //You have to perform the sync gesture to receive Pose data!
  Serial.println("update!");
}

void loop() {
  //update the connection to MyoBridge
  //  Serial.println("bridge!");
  bridge.update();
  
}
