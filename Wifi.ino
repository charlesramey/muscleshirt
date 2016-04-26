#include <SparkFunESP8266WiFi.h>

// Replace these two character strings with the name and
// password of your WiFi network.
//const char mySSID[] = "GTother";
//const char myPSK[] = "GeorgeP@1927";
const char mySSID[] = "MathewsWireless";
const char myPSK[] = "3956MathewsWAP"; // pls don't hack me

//IP address of whatever is hosting the "server"
const String recvServer = "192.168.1.80";
//const String recvServer = "128.61.19.153";

// my LED pin
int ledPin = 13;
int switchPin = 12;

int recording = 0;
int buttonDown = 0;

long prevTime = 0;

//my client object
ESP8266Client client;

void setup() {

  pinMode(ledPin, OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);
  
  // Serial Monitor is used to control the demo and view
  // debug information.
  Serial.begin(115200);
  delay(1000);
  
  // initializeESP8266() verifies communication with the WiFi
  // shield, and sets it up.
  initializeESP8266();
  delay(1000);

  // connectESP8266() connects to the defined WiFi network.
  while(connectESP8266()<0)
    delay(2000);

  // displayConnectInfo prints the Shield's local IP
  // and the network it's connected to.
  displayConnectInfo();

  // setup the server
//  connectToServer();
}

void loop() 
{
  // Sometimes stops/starts the recording
  // Sometimes cycles through both states several times, randomly choosing one
  if(!recording && !digitalRead(switchPin) && !buttonDown) {
    buttonDown = 1;
    recording = 1;
    Serial.println("start");
  } else if(recording && buttonDown && !digitalRead(switchPin)) {
    recording = 1;
    buttonDown = 1;
  } else if(recording && digitalRead(switchPin) && buttonDown) {
    recording = 1;
    buttonDown = 0;
    Serial.println("recording");
  } else if(recording && !digitalRead(switchPin) && !buttonDown) {
    recording = 0;
    buttonDown = 1;
    Serial.println("stop");
  } else if(!recording && digitalRead(switchPin) && buttonDown) {
    recording = 0;
    buttonDown = 0;
    Serial.println("not recording");
  }

  if(recording) {
    digitalWrite(ledPin, HIGH); // status light
    if( (millis() - prevTime) >= 1000) { //send every second without a blocking delay() call so recording can stop
      prevTime = millis();
      sendToServer();
    }
  } else {
    digitalWrite(ledPin, LOW); // status light
  }
  
}

void sendToServer() {
  Serial.println(client.status());
  int con = client.connect(recvServer, 3651);
  Serial.println(con);
  if(con <= 0) {
    Serial.println(F("No connection with server, retrying connection..."));
    return;
  }

  //TODO: Get actual values from devices

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

  Serial.print("sending: ");
  Serial.println(params);
  
  client.write(params.c_str(), strlen(params.c_str()));

  // Don't think this is necessary
  while (client.available()) // While there's data available
    Serial.write(client.read()); // Read it and print to serial
  
  client.stop();
}

//No longer used since the sendToServer() already connects
void connectToServer() {
  if(client.connect(recvServer, 3651) <= 0) {
    Serial.println(F("Failed to connect to server"));
    return;
  }
  Serial.println(F("Connected"));
}

void initializeESP8266()
{
  // esp8266.begin() verifies that the ESP8266 is operational
  // and sets it up for the rest of the sketch.
  // It returns either true or false -- indicating whether
  // communication was successul or not.
  // true
  int test = esp8266.begin();
  if (test != true)
  {
    Serial.println(F("Error talking to ESP8266."));
    errorLoop(test);
  }
  Serial.println(F("ESP8266 Device Present"));

  esp8266.reset();
  Serial.println(F("reset"));
  delay(1000);

  esp8266.echo(0);
  Serial.println(F("echo off"));
  
  // write the version information to the debug console
#define VERSIONBUFFERLENGTH 32
  char ATversion[VERSIONBUFFERLENGTH], SDKversion[VERSIONBUFFERLENGTH], compileTime[VERSIONBUFFERLENGTH];
  memset(ATversion, '\0', VERSIONBUFFERLENGTH);
  memset(SDKversion, '\0', VERSIONBUFFERLENGTH);
  memset(compileTime, '\0', VERSIONBUFFERLENGTH);
  esp8266.getVersion(ATversion, SDKversion, compileTime);  
  Serial.print(F("AT version: "));
  Serial.println(ATversion);
  Serial.print(F("SDK version: "));
  Serial.println(SDKversion);
  Serial.print(F("Compile time: "));
  Serial.println(compileTime);
}

int connectESP8266()
{
  // The ESP8266 can be set to one of three modes:
  //  1 - ESP8266_MODE_STA - Station only
  //  2 - ESP8266_MODE_AP - Access point only
  //  3 - ESP8266_MODE_STAAP - Station/AP combo
  // Use esp8266.getMode() to check which mode it's in:
  int retVal = esp8266.getMode();
  if (retVal != ESP8266_MODE_STA)
  { 
    // If it's not in station mode.
    // Use esp8266.setMode([mode]) to set it to a specified
    // mode.
    retVal = esp8266.setMode(ESP8266_MODE_STA);
    if (retVal < 0)
    {
      Serial.println(F("Error setting mode."));
      errorLoop(retVal);
    }    
  }
  Serial.println(F("Mode set to station"));

  // allow multiple TCP connections
  esp8266.setMux(1);  
  Serial.println(F("Multiple TCP connections set"));

  // esp8266.status() indicates the ESP8266's WiFi connect
  // status.
  // A return value of 1 indicates the device is already
  // connected. 0 indicates disconnected. (Negative values
  // equate to communication errors.)
  retVal = esp8266.status();
  if (retVal <= 0)
  {
    Serial.print(F("Connecting to "));
    Serial.println(mySSID);
    
    // esp8266.connect([ssid], [psk]) connects the ESP8266
    // to a network.
    // On success the connect function returns a value >0
    // On fail, the function will either return:
    //  -1: TIMEOUT - The library has a set 30s timeout
    //  -3: FAIL - Couldn't connect to network.
    retVal = esp8266.connect(mySSID, myPSK);
    
    if (retVal < 0)
      Serial.println(F("Error connecting"));
  }
  
  return retVal;
}

void displayConnectInfo()
{
  char connectedSSID[24];
  memset(connectedSSID, 0, 24);
  // esp8266.getAP() can be used to check which AP the
  // ESP8266 is connected to. It returns an error code.
  // The connected AP is returned by reference as a parameter.
  int retVal = esp8266.getAP(connectedSSID);
  if (retVal > 0)
  {
    Serial.print(F("Connected to: "));
    Serial.println(connectedSSID);
  }

  // esp8266.localIP returns an IPAddress variable with the
  // ESP8266's current local IP address.
  IPAddress myIP = esp8266.localIP();
  Serial.print(F("My IP: ")); Serial.println(myIP);

  // and also write the MAC address for LAWN registration
  Serial.print(F("Register this MAC address with GT Lawn "));
  char localMAC[24];
  int retval = esp8266.localMAC(&localMAC[0]);  
  Serial.println(localMAC);
}

// errorLoop prints an error code, then loops forever.
void errorLoop(int error)
{
  Serial.print(F("Error: ")); Serial.println(error);
  Serial.println(F("Looping forever."));
  for (;;);
}
