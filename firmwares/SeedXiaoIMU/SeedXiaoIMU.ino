#include "LSM6DS3.h"
#include "Wire.h"

#define OUTPUT__BAUD_RATE 57600

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

const int UPDATE_RATE = 20;
const float AXIS_DRIFT[] = {-0.9286f, 2.5988f, 0.48727f};
const float AXIS_SCALAR[] = {1.268f, 1.286f, 1.267f};

float angVel[] = {0.f, 0.f, 0.f};
float angPose[] = {0.f, 0.f, 0.f};
float linAcel[] = {0.f, 0.f, 0.f};

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

void loop() {
    readOrin();
    readGyro();
    readAcel();

    printAll(angPose, linAcel, angVel);

    delay(UPDATE_RATE);
}
