import serial
import yaml

from config_ref import *


class ConfigWriter():
    def __init__(self, serial_ : serial.Serial, config : yaml):
        self.ser_ = serial_
        self.cnf_ = config

        self.device : str = self.cnf_[SerialRef.SERIAL.value][SerialRef.DEVICE.value]

        print("[INFO]: Writing calibration data...")

        if (self.device in SupportedDevices._value2member_map_):
            self.calib()
        else:
            print("[WARN]: No config information for device: " + self.device)

        print("[INFO]: Good to go!")

    def calib(self):
        print("[INFO]: Configuring " + self.device)
        for entry in self.cnf_[CalibRef.CALIB.value][self.device][CalibRef.CMD.value]:
            cmd = self.cnf_[CalibRef.CALIB.value][self.device][CalibRef.CMD.value][entry]
            val = self.cnf_[CalibRef.CALIB.value][self.device][CalibRef.VAL.value][entry]
            self.ser_.write((str(cmd) + str(val)).encode(EncodingFormat.UTF_8.value))
            
