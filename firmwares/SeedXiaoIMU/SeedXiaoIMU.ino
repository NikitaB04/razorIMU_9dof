#include "LSM6DS3.h"
#include "Wire.h"

#define OUTPUT__BAUD_RATE 57600

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

int UPDATE_RATE = 20;

float AXIS_DRIFT[] = {0.f, 0.f, 0.f};
float AXIS_SCALAR[] = {1.f, 1.f, 1.f};

float GYRO_DRIFT[] = {0.f, 0.f, 0.f};
float GYRO_SCALAR[] = {1.f, 1.f, 1.f};

float ACEL_DRIFT[] = {0.f, 0.f, 0.f};
float ACEL_SCALAR[] = {1.f, 1.f, 1.f};

float angVel[] = {0.f, 0.f, 0.f};
float angPose[] = {0.f, 0.f, 0.f};
float linAcel[] = {0.f, 0.f, 0.f};

float calibMem[] = {0.f, 0.f, 0.f};

bool output_yprag = true;
int counter = 0;

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
    angPose[0] = angPose[0] + ( myIMU.readFloatGyroX() * (UPDATE_RATE  / 1000.0) ) - AXIS_DRIFT[0];
    angPose[1] = angPose[1] + ( myIMU.readFloatGyroY() * (UPDATE_RATE  / 1000.0) ) - AXIS_DRIFT[1];
    angPose[2] = angPose[2] + ( myIMU.readFloatGyroZ() * (UPDATE_RATE  / 1000.0) ) - AXIS_DRIFT[2];

    counter++;
}

void readGyro() {
    float x,y,z;
    x = ( myIMU.readFloatGyroX() - GYRO_DRIFT[0] ) * GYRO_SCALAR[0];
    y = ( myIMU.readFloatGyroY() - GYRO_DRIFT[1] ) * GYRO_SCALAR[1];
    z = ( myIMU.readFloatGyroZ() - GYRO_DRIFT[2] ) * GYRO_SCALAR[2];

    angVel[0] = x;
    angVel[1] = y;
    angVel[2] = z;
}

void readAcel() {
    float x,y,z;
    x = ( myIMU.readFloatAccelX() - ACEL_DRIFT[0] ) * ACEL_SCALAR[0];
    y = ( myIMU.readFloatAccelY() - ACEL_DRIFT[1] ) * ACEL_SCALAR[1];
    z = ( myIMU.readFloatAccelZ() - ACEL_DRIFT[2] ) * ACEL_SCALAR[2];

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

        if (type_param == 'o') {
          char param_param = readChar();
          char axis_param = readChar();
          float value_param = Serial.parseFloat();
          if (param_param == 'd') {
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
          if (param_param == 's') {
            if (axis_param == 'x') {
              AXIS_SCALAR[0] = value_param;
            } else
            if (axis_param == 'y') {
              AXIS_SCALAR[1] = value_param;
            } else
            if (axis_param == 'z') {
              AXIS_SCALAR[2] = value_param;
            }
          }
        } else

        if (type_param == 'g') {
          char param_param = readChar();
          char axis_param = readChar();
          float value_param = Serial.parseFloat();
          if (param_param == 'd') {
            if (axis_param == 'x') {
              GYRO_DRIFT[0] = value_param;
            } else
            if (axis_param == 'y') {
              GYRO_DRIFT[1] = value_param;
            } else
            if (axis_param == 'z') {
              GYRO_DRIFT[2] = value_param;
            }
          } else
          if (param_param == 's') {
            if (axis_param == 'x') {
              GYRO_SCALAR[0] = value_param;
            } else
            if (axis_param == 'y') {
              GYRO_SCALAR[1] = value_param;
            } else
            if (axis_param == 'z') {
              GYRO_SCALAR[2] = value_param;
            }
          }
        } else

        if (type_param == 'a') {
          char param_param = readChar();
          char axis_param = readChar();
          float value_param = Serial.parseFloat();
          if (param_param == 'd') {
            if (axis_param == 'x') {
              ACEL_DRIFT[0] = value_param;
            } else
            if (axis_param == 'y') {
              ACEL_DRIFT[1] = value_param;
            } else
            if (axis_param == 'z') {
              ACEL_DRIFT[2] = value_param;
            }
          } else
          if (param_param == 's') {
            if (axis_param == 'x') {
              ACEL_SCALAR[0] = value_param;
            } else
            if (axis_param == 'y') {
              ACEL_SCALAR[1] = value_param;
            } else
            if (axis_param == 'z') {
              ACEL_SCALAR[2] = value_param;
            }
          }
        } else
        
        if (type_param == 'u') {
          UPDATE_RATE = Serial.parseInt();
        }
      } else

      if (command == '0') {
        angVel[0] = 0.f;
        angVel[1] = 0.f;
        angVel[2] = 0.f;
        angPose[0] = 0.f;
        angPose[1] = 0.f;
        angPose[2] = 0.f;
        linAcel[0] = 0.f;
        linAcel[1] = 0.f;
        linAcel[2] = 0.f;
      } else

      if (command == 's') {
        Serial.print("X_DRIFT: "); Serial.println((angPose[0]-calibMem[0]) * 1000000 / counter);
        Serial.print("Y_DRIFT: "); Serial.println((angPose[1]-calibMem[1]) * 1000000 / counter);
        Serial.print("Z_DRIFT: "); Serial.println((angPose[2]-calibMem[2]) * 1000000 / counter);

        calibMem[0] = angPose[0];
        calibMem[1] = angPose[1];
        calibMem[2] = angPose[2];
        counter = 0;
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
