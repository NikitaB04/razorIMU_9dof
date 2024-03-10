#include "LSM6DS3.h"
#include "Wire.h"

#define OUTPUT__BAUD_RATE 57600

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

int UPDATE_RATE = 20;
float AXIS_DRIFT[] = {0.f, 0.f, 0.f};
float AXIS_SCALAR[] = {1.f, 1.f, 1.f};

float angVel[] = {0.f, 0.f, 0.f};
float angPose[] = {0.f, 0.f, 0.f};
float linAcel[] = {0.f, 0.f, 0.f};

bool output_yprag = true;

void setup() {
    Serial.begin(57600);
    while (!Serial);
    if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        Serial.println("Device OK!");
    }
}

void printAll(float gyro[], float acel[], float rot[]) {
  // #YPRAG=4.60,40.62,160.75,-156.61,51.52,-162.58,-0.19,-0.06,0.35
  Serial.print("#YPRAG=");
  Serial.print(gyro[0] * AXIS_SCALAR[0]); Serial.print(",");
  Serial.print(gyro[1] * AXIS_SCALAR[1]); Serial.print(",");
  Serial.print(gyro[2] * AXIS_SCALAR[2]); Serial.print(",");
  
  Serial.print(acel[0]); Serial.print(",");
  Serial.print(acel[1]); Serial.print(",");
  Serial.print(acel[2]); Serial.print(",");

  Serial.print(rot[0]); Serial.print(",");
  Serial.print(rot[1]); Serial.print(",");
  Serial.print(rot[2]); Serial.println();
}

void readOrin() {
    angPose[0] = angPose[0] + ( (myIMU.readFloatGyroX() + AXIS_DRIFT[0]) / 1000) * UPDATE_RATE;
    angPose[1] = angPose[1] + ( (myIMU.readFloatGyroY() + AXIS_DRIFT[1]) / 1000) * UPDATE_RATE;
    angPose[2] = angPose[2] + ( (myIMU.readFloatGyroZ() + AXIS_DRIFT[2]) / 1000) * UPDATE_RATE;
}

void readGyro() {
    float x,y,z;
    x = myIMU.readFloatGyroX();
    y = myIMU.readFloatGyroY();
    z = myIMU.readFloatGyroZ();

    angVel[0] = x;
    angVel[1] = y;
    angVel[2] = z;
}

void readAcel() {
    float x,y,z;
    x = myIMU.readFloatAccelX();
    y = myIMU.readFloatAccelY();
    z = myIMU.readFloatAccelZ();

    linAcel[0] = x;
    linAcel[1] = y;
    linAcel[2] = z;
}

// Blocks until another byte is available on serial port
char readChar()
{
  while (Serial.available() < 1) { }
  return Serial.read();
}

void readCommands() {
  if (Serial.available() >= 2) {
    if (Serial.read() == '#') {
      int command = Serial.read();
      if (command == 'o') {
        char output_type = readChar();
        if (output_type == '0') {
          output_yprag = false;
        } else if (output_type == '1') {
          output_yprag = true;
        }
      } else

      if (command == 'c') {
        char type_param = readChar();

        if (type_param == 'd') {
          char axis_param = readChar();
          float value_param = Serial.parseFloat();
          if (axis_param == 'x') {
            AXIS_DRIFT[0] = value_param;
          } else
          if (axis_param == 'y') {
            AXIS_DRIFT[1] = value_param;
          } else
          if (axis_param == 'z') {
            AXIS_DRIFT[2] = value_param;
          }
        } else

        if (type_param == 's') {
          char axis_param = readChar();
          float value_param = Serial.parseFloat();
          if (axis_param == 'x') {
            AXIS_SCALAR[0] = value_param;
          } else
          if (axis_param == 'y') {
            AXIS_SCALAR[1] = value_param;
          } else
          if (axis_param == 'z') {
            AXIS_SCALAR[2] = value_param;
          }
        } else
        
        if (type_param == 'u') {
          UPDATE_RATE = Serial.parseInt();
        }
      }
    }
  }
}

void loop() {
    readCommands();

    readOrin();
    readGyro();
    readAcel();

    if (output_yprag) {
      printAll(angPose, linAcel, angVel);
    }

    delay(UPDATE_RATE);
}
