//Serial:ComputertoTeensy
//Serial1:TeensytoESP8266modem
void setup()
{
  //SetupcomputertoTeensyserial
  Serial.begin(115200);
  //SetupTeensytoESP8266serial
  //Usebaudrate115200duringfirmwareupdate
  Serial1.begin(115200);
  Serial1.write("AT\r\n");
  delay(500);
  Serial1.write("AT+CWMODE=1\r\n");
  delay(2000);
  Serial1.write("AT+CWJAP=\"ESP\",\"abc\"\r\n");
  delay(8000);
  Serial1.write("AT+CIPMUX=1\r\n");
  delay(8000);
  Serial1.write("AT+CIPSTART=1,\"TCP\",\"192.168.4.1\",3651\r\n");
  delay(8000);
  Serial1.write("AT+CIPSEND=1,3\r\n");
  delay(500);
  Serial1.write("HI\r");
  delay(500);
  //Serial1.write("AT+CIPCLOSE=0");
}
void loop()
{
//  //SendbytesfromESP8266‐>TeensytoComputer
//  if(Serial1.available())
//  Serial.write(Serial1.read());
//  //SendbytesfromComputer‐>TeensybacktoESP8266
//  if(Serial.available())
//  Serial1.write(Serial.read());
  Serial1.write("AT+CIPSEND=1,3\r\n");
  delay(50);
  Serial1.write("HI\r");
  delay(50);
}
