// Serial : Computer to Teensy 
// Serial1 : Teensy to ESP8266 modem 

int stepNum = 1;

int counter = 0;
int isDone = 0;

int recording = 0;

long prevTime = 0;

int switchPin = 12;
int ledPin = 13;

int state = 0;
 
void setup()  
{  
    
    pinMode(ledPin, OUTPUT);
    
    pinMode(switchPin, INPUT_PULLUP);
    
    // Setup computer to Teensy serial 
    Serial.begin(115200); 
 
    // Setup Teensy to ESP8266 serial 
    // Use baud rate 115200 during firmware update 
    Serial1.begin(115200);
    
    Serial1.write("AT+CWMODE=2\r\n");
    delay(500);
    Serial1.write("AT+CWSAP=\"ESP\",\"abc\",5,0\r\n");
    delay(500);
    Serial1.write("AT+CIPMUX=1\r\n");
    delay(500);
    Serial1.write("AT+CIPSERVER=1,3651\r\n");
    delay(500);
} 
 
void loop()  
{ 
  // set up
//    if(stepNum == 1) {
//      Serial1.write("AT+CWMODE=2\r\n");
//      delay(500);
//      stepNum = 2;
//    } else if(stepNum == 2) {
//      Serial1.write("AT+CWSAP=\"ESP\",\"abc\",5,0\r\n");
//      delay(500);
//      stepNum=3;
//    } else if(stepNum == 3) {
//      Serial1.write("AT+CIPMUX=1\r\n");
//      delay(500);
//      stepNum = 4;
//    } else if(stepNum == 4) {
//      Serial1.write("AT+CIPSERVER=1,3651\r\n");
//      delay(500);
//      stepNum = 5;
//    }

    int sw = digitalRead(switchPin); // 0 when pressed, 1 otherwise
    if(state == 0) {
      if(sw) {
        state = 0;
      } else {
        state = 1;
      }
    } else if(state == 1) {
      if(sw) {
        state = 2;
      } else {
        state = 1;
      }
    } else if(state == 2) {
      if(sw) {
        state = 2;
      } else {
        state = 3;
      }
    } else if(state == 3) {
      if(sw) {
        state = 0;
      } else {
        state = 3;
      }
    }

    if(state == 2 || state == 3) {
      recording = 1;
      digitalWrite(ledPin, HIGH);
//      Serial.println("recording");
    } else {
      digitalWrite(ledPin, LOW);
//      Serial.println("not recording");
      recording = 0;
    }

    delay(10);

    if(recording) {
      if(Serial1.available()) {
        String request = Serial1.readString();
        Serial.println(request);

        if(request.indexOf("+IPD") >= 0) {
          sendData();
        }
      }
    } else { // just print the data the serial port sees
      if(Serial1.available()) 
        Serial.write(Serial1.read());
      
      // Send bytes from Computer ‐> Teensy back to ESP8266 
      if ( Serial.available() )  
        Serial1.write( Serial.read() );   
    }
    
    
    
}

void sendDone() {
  String s = "done";

  Serial1.write(("AT+CIPSEND=0," + String(s.length()) + "\r\n").c_str());

  delay(500);
  
  Serial1.write(s.c_str());  
}

void sendData() {
  float emg_f = 606, emg_b = 323, emg_p = 124;

  float f_pitch = 3.1, f_roll = 1.3;
  float b_pitch = 2.4, b_roll = 4.2;
  

  String params = "";
  params += "EMG_forearm: " + String(emg_f) + ", ";
  params += "EMG_bicep: " + String(emg_b) + ", ";
  params += "EMG_pec: " + String(emg_p) + ", ";
  params += "Pitch_forearm: " + String(f_pitch) + ", ";
  params += "Roll_forearm: " + String(f_roll) + ", ";
  params += "Pitch_bicep: " + String(b_pitch) + ", ";
  params += "Roll_bicep: " + String(b_roll) + ";";
  params += "\r\n";

//  Serial.print("sending: ");
//  Serial.println(params);

  Serial.println("Sending " + String(params.length()) + " bytes");
  
  Serial1.write(("AT+CIPSEND=0," + String(params.length())).c_str());

  delay(50);
  
  Serial1.write(params.c_str());
}

