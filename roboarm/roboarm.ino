#include <Braccio.h>
#include <Servo.h>

#define MSG_METHOD_SUCCESS 0
#define MSG_METHOD_FAIL 1
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

void setup() {  
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Serial.begin(9600);
  Serial.println("not sure if I'm sane");

  Braccio.begin();
}

void loop() {
  //Serial Input Section -- handles commands received from software
  String command = "";  //Used to store the latest received command
  int serialResult = 0; //return value for reading operation method on serial in put buffer
  serialResult = readSerialInputCommand(&command);  
  if (serialResult == MSG_METHOD_SUCCESS)
  {
    Serial.println("Got a message:");
    Serial.println(command);
    if(command.substring(0,5)=="servo")
    {
      String parseString = command.substring(5,8);
      int M2 = parseString.toInt();
      parseString = command.substring(8,11);
      int M3 = parseString.toInt();
      parseString = command.substring(11,14);
      int M4 = parseString.toInt();
      parseString = command.substring(14,17);
      int M5 = parseString.toInt();
      Braccio.ServoMovement(11, 45, M2, M3, M4, M5, 73);  
    }
  }
}

int readSerialInputCommand(String *command)
{
  int operationStatus = MSG_METHOD_FAIL;//Default return is MSG_METHOD_FAIL reading data from com buffer.

  //check if serial data is available for reading
  if (Serial.available())
  {
    char serialInByte;//temporary variable to hold the last serial input buffer character

    while (serialInByte != '#' && Serial.available()) //until '#' comes up or no serial data is available anymore
    {
      serialInByte = Serial.read();
      *command = *command + serialInByte;//Add last read serial input buffer byte to *command pointer
      delay(10);
    }
    operationStatus = MSG_METHOD_SUCCESS;
  }
  return operationStatus;
}

