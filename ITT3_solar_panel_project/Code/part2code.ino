#include <Wire.h>
#include <WiFiNINA.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>
// Calculations variables for the gyro and accl
float thetaM;
float phiM;
float thetaFold = 0;
float thetaFnew;
float phiFold = 0;
float phiFnew;

float thetaG = 0;
float phiG = 0;

float theta;
float phi;

float dtime;
unsigned long millisOld;

// Variables
int buttonState = 0;         // variable for reading the pushbutton status

// Pinouts
const int buttonPin = 13;     // the number of the pushbutton pin
const int ledPinGreen =  17;      // the number of the LED pin
const int ledPinYellow =  20; 
const int ledPinRed =  21;
const int Buzzer =  16; 

// Defined variables
#define BNO055_SAMPLERATE_DELAY_MS (100)
#define taG_UPPERBOUND (40) // Setting the limitation for the thetaG on the up signal.
#define taG_LOWERBOUND (-40) // Setting the limitation for the thetaG on the down signal.
#define phi_UPPERBOUND (40) // Setting for the limitaition for the Phi on the left signal.
#define phi_LOWERBOUND (-40) // Setting for the limitation for the Phi on the right signal.


Adafruit_BNO055 myIMU = Adafruit_BNO055();

void setup() {
// put your setup code here, to run once:
  Wire.begin();
  Serial.begin(115200);
  myIMU.begin();
  delay(1000);
//  int8_t temp = myIMU.getTemp();
  myIMU.setExtCrystalUse(true);
  millisOld = millis();
  
// initialize the LED pin as an output:
  pinMode(ledPinGreen, OUTPUT);
  pinMode(ledPinYellow, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(Buzzer, OUTPUT);
  
// initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);


}

void loop() {
//Gyro Code For the BNO
  uint8_t system, gyro, accel, mg = 0;
  myIMU.getCalibration(&system, &gyro, &accel, &mg);
  imu::Vector<3> acc = myIMU.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  imu::Vector<3> gyr = myIMU.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  
  thetaM = -atan2(acc.x() / 9.8, acc.z() / 9.8) / 2 / 3.141592654 * 360;
  phiM = -atan2(acc.y() / 9.8, acc.z() / 9.8) / 2 / 3.141592654 * 360;
  phiFnew = .95 * phiFold + .05 * phiM;
  thetaFnew = .95 * thetaFold + .05 * thetaM;
  
  dtime = (millis() - millisOld) / 1000.;
  millisOld = millis();
  theta = (theta + gyr.y() * dtime) * .95 + thetaM * .05;
  phi = (phi - gyr.x() * dtime) * .95 + phiM * .05;
  thetaG = thetaG + gyr.y() * dtime;
  phiG = phiG - gyr.x() * dtime;
  
// Serial print, as for use in Vpython.
  Serial.print(",");
  Serial.print(thetaG);
  Serial.print(",");
  Serial.print(phiG);
  Serial.print(",");
  Serial.print(theta);
  Serial.print(",");
  Serial.println(phi);
  
  phiFold = phiFnew;
  thetaFold = thetaFnew;
    
// Safety code based on the BNO mesurements. ment to protect the solar panel from breaking the motor.
  if(thetaG > taG_UPPERBOUND) {
    digitalWrite(10, LOW);
  } else if(thetaG < taG_LOWERBOUND) {
    digitalWrite(9, LOW);
  } else if(phi > phi_UPPERBOUND) {
    digitalWrite(8, LOW);
  } else if (phi < phi_LOWERBOUND){
    digitalWrite(7, LOW);
  }

//GUI Code
  if (Serial.available()) { //id data is available to read

    char val = Serial.read();

// Button Pinout
  if (val == 'u'){
    digitalWrite(10, HIGH); // Up Signal
  } else if (val == 'd'){
    digitalWrite(9, HIGH); // Down Signal
  } else if (val == 'r'){
    digitalWrite(8, HIGH); // Left Signal
  } else if (val == 'l'){
    digitalWrite(7, HIGH); // Right Signal
  }
  

// Stop Signal Sets all pinout to LOW
  if (val == 's') {
    digitalWrite(10, LOW);
    digitalWrite(9, LOW);
    digitalWrite(8, LOW);
    digitalWrite(7, LOW);
   }
  }

//LED 

// read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

// check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    analogWrite(ledPinGreen, 255);
    analogWrite(ledPinYellow, 255);
    analogWrite(ledPinRed, 255);
    analogWrite(Buzzer, 150);
   
    
  }
  else {
    // turn LED off:
    analogWrite(ledPinGreen, 0);
    analogWrite(ledPinYellow, 0);
    analogWrite(ledPinRed, 0);
    analogWrite(Buzzer, 0);
    
    
  }

  
// This is more for reading the serial print out log rather then functional use.
delay(BNO055_SAMPLERATE_DELAY_MS);
}
