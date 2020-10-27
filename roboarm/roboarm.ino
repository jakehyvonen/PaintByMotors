#include <Braccio.h>
#include <Servo.h>

#define MSG_METHOD_SUCCESS 0
#define MSG_METHOD_FAIL 1
Servo base;//M1
Servo shoulder;//M2
Servo elbow;//M3
Servo wrist_rot;//M4
Servo wrist_ver;//M5
Servo gripper;//M6
int del=11, M1=90, M2=11, M3=111, M4=1, M5=90, M6=73;
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
  //Serial.println("not sure if I'm sane");
  Braccio.begin();//-999 == Braccio.SOFT_START_DISABLED
  //Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6);  
}

void loop() {
  //Serial Input Section -- handles commands received from software
  String command = "";  //Used to store the latest received command
  int serialResult = 0; //return value for reading operation method on serial in put buffer
  serialResult = readSerialInputCommand(&command);  
  if (serialResult == MSG_METHOD_SUCCESS)
  {
    //Serial.println("Got a message:");
    //Serial.println(command);
    //servos M1 and M6 are not physically used
    //so we only interact with M2-M5 values
    if(command.substring(0,4)=="echo")
    {
      String parseString = command.substring(4,7);
      M2 = parseString.toInt();
      parseString = command.substring(7,10);
      M3 = parseString.toInt();
      parseString = command.substring(10,13);
      M4 = parseString.toInt();
      parseString = command.substring(13,16);
      M5 = parseString.toInt();
      Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6);  
      Serial.println(String(M2)+","+String(M3)+","+String(M4)+","+String(M5));
    }
    else if(command.substring(0,3)=="get")
    {
      Serial.println(String(M2)+","+String(M3)+","+String(M4)+","+String(M5));
    }     
    else if(command.substring(0,4)=="ping")
    {
      Serial.println("pong");
    }
    else if(command.substring(0,3)=="set")
    {
      String parseString = command.substring(3,6);
      M2 = parseString.toInt();
      //Serial.print("M2: " + String(M2));
      parseString = command.substring(6,9);
      M3 = parseString.toInt();
      //Serial.print(" M3: " + String(M3));
      parseString = command.substring(9,12);
      M4 = parseString.toInt();
      //Serial.print(" M4: " + String(M4));
      parseString = command.substring(12,15);
      M5 = parseString.toInt();
      //Serial.print(" M5: " + String(M5));
      Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6);  
      serial.println('ok')
    }
    else if(command.substring(0,4)=="open")
    {
      //String parseString = command.substring(4,7);
      //M1 = parseString.toInt();
      M1 = 77;
      Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6);
      serial.println('ok')
    }
    else if(command.substring(0,5)=="rinse")
    {
      M1 = 160;
      Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6); 
      serial.println('ok')
    }
    else if(command.substring(0,5)=="close")
    {
      M1 = 163;
      Braccio.ServoMovement(del, M1, M2, M3, M4, M5, M6);
      serial.println('ok')
    }
    else
    {
      Serial.println("Unrecognized command. Please check roboarm.ino for reference");
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
