#include "SerialTransfer.h"
#include <Stepper.h>


SerialTransfer myTransfer;
const int stepsPerRevolution = 2038;
const int timeOfStep = 0;
const int timeOfZ = 0;
const int stepsZ = 0;
const int weeder = 0;
const int pump = 0;
const int soilMoist = A0;
const int soilMoistPower = 0;
Stepper x1 = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper x2 = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper y1 = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper y2 = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper z1 = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper z2 = Stepper(stepsPerRevolution, 8, 10, 9, 11);

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  
  x1.setSpeed(5);
  x2.setSpeed(5);
  y1.setSpeed(5);
  y2.setSpeed(5);
  z1.setSpeed(5);
  z2.setSpeed(5);
  pinMode(weeder, OUTPUT);
  pinMode(pump, OUTPUT);
  pinMode(soilMoist, INPUT);
  pinMode(soilMoistPower, OUTPUT);
}

void loop()
{
  int*sgX = NULL;
  int*sgY = NULL;
  int*sbX = NULL;
  int*sbY = NULL;
  int*incomingArray = NULL;
  
while (!myTransfer.available())
  {
    delay(10);
  }

  for (int i = 0; i < 4; i++)
  {
      if(myTransfer.available())  
      { 
        free(incomingArray);
        int arraySize = myTransfer.bytesRead / sizeof(int);
        incomingArray = (int*)malloc(arraySize * sizeof(int));
    
        String incomingString ="";
    
        for (uint16_t i = 0; i < myTransfer.bytesRead; i++)
        {
         myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
         incomingString += (char)myTransfer.packet.rxBuff[i];
        }
          
        for (uint16_t i = 0; i < arraySize; i++) 
        {
        incomingArray[i] = *((int*)(myTransfer.packet.rxBuff + i * sizeof(int)));
        }
        
        if (incomingString == "sgX")
        {
          if (sgX != NULL) 
          {
            free(sgX);
          }
          sgX = (int*)malloc(arraySize*sizeof(int));
          if (sgX != NULL) 
          { 
            for (int i = 0; i < arraySize; i++)
            {
              sgX[i] = incomingArray[i];
            }
          }
        }
    
        if (incomingString == "sgY")
        {
          if (sgY != NULL) 
          {
            free(sgY);
          }
          sgY = (int*)malloc(arraySize*sizeof(int)); 
          if (sgY != NULL) 
          {
            for (int i = 0; i < arraySize; i++)
            {
              sgY[i] = incomingArray[i];
            }
          }
        }
        
        if (incomingString == "sbX")
        {
          if (sbX != NULL) 
          {
            free(sbX);
          }
          sbX = (int*)malloc(arraySize*sizeof(int));
          if (sbX != NULL) 
          { 
            for (int i = 0; i < arraySize; i++)
            {
              sbX[i] = incomingArray[i];
            }
          }
        }
    
        if (incomingString == "sbY")
        {
          if (sbY != NULL) 
          {
            free(sbY);
          }
          sgY = (int*)malloc(arraySize*sizeof(int));
          if (sbY != NULL) 
          { 
            for (int i = 0; i < arraySize; i++)
            {
              sbY[i] = incomingArray[i];
            }
          }
        }
        myTransfer.sendData(myTransfer.bytesRead);
       }
  }

  if(myTransfer.available())
  { 
   for (uint16_t i = 0; i < myTransfer.bytesRead; i++) 
   {
    myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
   }
  }

  
  if (sbX != NULL)
  {
    int sbXSize = sizeof(sbX);
    int oldStepsX = 0;
    int oldStepsY = 0;
    
    for (int i = 0; i < sbXSize; i++)
    {
     int mapX = map(sbX[i],0,640,0,0);// last maxStepsX
     int mapY = map(sbY[i],0,480,0,0);// last maxStepsY
     
      int stepsX = (mapX - oldStepsX)*stepsPerRevolution;
     int stepsY = (mapY - oldStepsY)*stepsPerRevolution;
     
     int timeX = stepsX*timeOfStep;
     int timeY = stepsY*timeOfStep;
     
     x1.step(stepsX);
     x2.step(stepsX);
     delay(timeX);
      
     y1.step(stepsY);
     y2.step(stepsY);
     delay(timeY);
     
     z1.step(stepsZ);
     z2.step(stepsZ);
     delay(timeOfZ);
     
     digitalWrite(weeder, HIGH);
     delay(0);
     digitalWrite(weeder, LOW);
     
     z1.step(-stepsZ);
     z2.step(-stepsZ);
     delay(timeOfZ);
     
     oldStepsX = mapX;
     oldStepsY = mapY;
    }
   }
  if (sgX != NULL)
   {
    int sgXSize = sizeof(sgX);
    int oldStepsX = 0;
    int oldStepsY = 0;
    
    for (int i = 0; i < sgXSize; i++)
    {
     int mapX = map(sgX[i],0,640,0,0);// last maxStepsX
     int mapY = map(sgY[i],0,480,0,0); // last maxStepsY
     
     int stepsX = (mapX - oldStepsX)*stepsPerRevolution;
     int stepsY = (mapY - oldStepsY)*stepsPerRevolution;
     
     int timeX = stepsX*timeOfStep;
     int timeY = stepsY*timeOfStep;
     
     x1.step(stepsX);
     x2.step(stepsX);
     delay(timeX);
      
     y1.step(stepsY);
     y2.step(stepsY);
     delay(timeY);
     
     z1.step(stepsZ);
     z2.step(stepsZ);
     delay(timeOfZ);
     
     digitalWrite(soilMoistPower, HIGH);
     int moist = analogRead(soilMoist);
     moist = map(moist, 0, 1023, 0, 100);
     digitalWrite(soilMoistPower, LOW);
     if(moist < 0)
     {
      digitalWrite(pump, HIGH);
      delay(0);
      digitalWrite(pump, LOW);
     }
     z1.step(-stepsZ);
     z2.step(-stepsZ);
     delay(timeOfZ);
      
     oldStepsX = mapX;
     oldStepsY = mapY;
    }   
   }
  myTransfer.sendData(myTransfer.bytesRead);
  free(sgX);
  free(sgY);
  free(sbX);
  free(sbY);
  }
