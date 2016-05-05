#define INPUT_SIZE 8

#include <string.h>

int lMotorPin = 20;
int rMotorPin = 21;

int rMotorSpeed = 0;
int lMotorSpeed = 0;

void setup() {
  // Setup computer to Teensy serial
  Serial.begin(115200);

  // Setup Teensy to ESP8266 serial
  Serial1.begin(115200);

  // set up wifi module
  //server and AP
  Serial1.write("AT+CWMODE=2\r\n");
  delay(500);
  Serial1.write("AT+CWSAP=\"ESP\",\"abc\",5,0\r\n");
  delay(500);
  Serial1.write("AT+CIPMUX=1\r\n");
  delay(500);
  Serial1.write("AT+CIPSERVER=1,3651\r\n");
  delay(500);
  
  Serial.println("Done setting up");
}

void loop() {

  // Send bytes from Computer ‐> Teensy back to ESP8266 
  if ( Serial1.available() ) { 
      if(Serial1.find(":")) {
        lMotorSpeed = Serial1.parseInt();
        rMotorSpeed = Serial1.parseInt();
      }
    }
    
    Serial.print("left: ");
    Serial.println(lMotorSpeed);
    Serial.print("right: ");
    Serial.println(rMotorSpeed);
    
    analogWrite(lMotorPin, lMotorSpeed);
    analogWrite(rMotorPin, rMotorSpeed);
  
  delay(50);
}

