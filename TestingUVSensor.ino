//Test UV Sensor and what value we get from UV Light
void setup() 
{
  //baud
  Serial.begin(9600);
}
 
void loop() 
{
  //intizialize values
  float sensorVoltage; 
  float sensorValue;
 //read
  sensorValue = analogRead(A0);
  sensorVoltage = sensorValue/1024*5;
  //print what it reads
  Serial.print("sensor reading = ");
  Serial.print(sensorValue);
  Serial.println("");
  Serial.print("sensor voltage = ");
  Serial.print(sensorVoltage);
  Serial.println(" V");
  delay(1000);
}
