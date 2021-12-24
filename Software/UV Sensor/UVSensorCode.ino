//LED Pin numbers, change after completing cirucit
const int red = 12;
const int green = 13;
const int sensorPin = A0;
//counters
int x= 0;
int y= 0;

//sensor values
float sensorVoltage;
float sensorValue;

void setup() {
  // initialize LEDs as an output.
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
}


void loop() {
  //Sensor Read
  sensorValue = analogRead(A0);
  sensorVoltage = (sensorValue/1024)*3.3 //If using 5 Volts instead of 3.3, change line
  //Red LED on and Green Off
  digitalWrite(green, LOW);   // turn the Green LED off 
  digitalWrite(red, HIGH);   // turn the LED on (HIGH is the voltage level)
  
 //while loop to signify UV is in area. Change voltage value after testing sensor
 //This assumes that 1 volt or greater means there's uv radiation in the area.
  if (sensorVotlage>=1){
   //turn off red LED
    digitalWrite(red, LOW);
  }
  //Values need to be changed after testing UV Sensor!
  while (1.1>=sensorVoltage>=1 && x<100) { //Further away from light but still senses it, this process takes ~50 seconds
    Processing();
    x+=4;
  }
  while (1.25>=sensorVoltage>=1.1 && x<100) { //This process takes ~40 seconds
    Processing();
    x+=5;
  }
  while (1.35>=sensorVoltage>1.25 && x<100) { //this process takes ~33 seconds
    Processing();
    x+=6;
  }
  while (1.5>=sensorVoltage>1.35 && x<100) { //Further away from light but still senses it, this process takes ~30 seconds
    Processing();
    x+=8;
  }
  while (1.75>= sensorVoltage>1.5 && x<100)  { //this range takes ~20 seconds
    Processing();
    x+=10;
  }
  while (2>= sensorVoltage>1.75 && x<100)  { //A little closer but still takes more time than if it were closer, this range takes ~14 seconds
    Processing();
    x+=15;
  }
    while (2.5>= sensorVoltage>2 && x<100)  { //Closest point and provides the highest voltage level, this range takes ~8 seconds
    Processing();
    x+=25;
  }
  if (100 > x > 0 && sensorVoltage<1){ //counter for seconds the uv light disapates before finishing cleaning.
    delay(1000);
    y +=1;
  }//Need to do something with this timer... How long does it go before it needs to restart clock?
  if (y>=10) {
    x = 0;
  }
    
 //Green LED ON
 if (x>=100){
 digitalWrite(red, LOW);
 digitalWrite(green, HIGH);   // turn the Green LED on
 }
}


void Processing() {
    //Every blink is one second. This process takes two seconds
    //Green LED Blinking
    digitalWrite(green, HIGH);   // turn the Green LED on
    delay(1000);                       // wait for a second
    digitalWrite(green, LOW);   // turn the Green LED off 
    delay(1000);                      // wait for a second 
} 
