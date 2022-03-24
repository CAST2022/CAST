//Test UV Sensor and what value we get from UV Light
//Ports for lights
const int red = 5;
const int green = 4;

const int numReadings = 200;//Number of readings to get 
float readings = 0;      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
float Average = 0;                // the average
//counters
int MainCounter = 0;
int Reset = 0;
int Finished = 0;

//sensor values
float UVDose;
float smoothing();


void setup()
{
  // initialize LEDs as an output.
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
}

void loop()
{
  //loop to signify UV is in area. Under 60 mW/cm^2 indicates no UV
  while (Average < 60 && Finished != 1)
  {
    smoothing(); //input function

    //Red LED on and Green Off. Initial Stage
    digitalWrite(green, LOW);   // turn the Green LED off
    digitalWrite(red, HIGH);   // turn the LED on (HIGH is the voltage level)
    //Delay one second
    delay(1000);

    //Add one second to reset counter
    Reset += 1;
    //if the reset counter hits 30 seconds, it resets the main counter
    if (Reset >= 30)
    {
      MainCounter = 0;
    }
  }

  while (Average >= 60 && Finished != 1) //60 mW/cm^2 is the minimum for UV intensity to blink green LED
  {
    smoothing();
    Reset = 0;
    //red LED turns off and green blinks to signify that area is being cleaned.
    digitalWrite(red, LOW);   // turn the LED off
    digitalWrite(green, HIGH);   // turn the Green LED on
    delay(500);
    digitalWrite(green, LOW);   // turn the Green LED off
    delay(500);
    MainCounter += 1;
    UVDose = (MainCounter * Average) / 1000;

    if (UVDose > 3.7) //Value you would need to change for threshold 
    {
      Finished = 1;
      break;
    }
  }

  if (Finished == 1)
  {
    digitalWrite(green, HIGH);   // turn the Green LED on
  }
}

float smoothing()
{
  total = 0;
  for (int count = 0; count < 199; count++)
  {
    readings = analogRead(A0)-8; //Reading inputs, subtractting to offset noise
    total = total + readings; //total readings together
  }
  // calculate the average, Converts Photocurrent Value to UV Intensity, uW/cm^2 (1uA = 9 mW/cm^2)
  Average = ((total / numReadings) * 9);
  return (Average);
}
