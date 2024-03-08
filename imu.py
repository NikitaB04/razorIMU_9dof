import time
import serial
import yaml
import threading

from config_ref import *
from config_writer import ConfigWriter

# Default acces values if config.yaml not found
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BOUNDRATE = 57600
DEFAULT_BOOT_TME = 2

class RazorIMU():
    def __init__(self, config_path=None):
        self.on = False
        self.has_config = False

        self.config = None
        self.port = DEFAULT_PORT
        self.boundrate = DEFAULT_BOUNDRATE
        self.boot_time = DEFAULT_BOOT_TME

        self.orient = {'x': 0., 'y': 0., 'z': 0.}
        self.accel = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.gyro = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.temp = None

        self.orin_scale = 1
        self.acel_scale = 1
        self.gyro_scale = 1


        try:
            with open(config_path, "r") as yamlfile:
                data = yaml.load(yamlfile, Loader=yaml.FullLoader)
                print("[INFO]: Got config file!")
                self.has_config = True
                self.config = data
                self.port = self.config[SerialRef.SERIAL.value][SerialRef.PORT.value]
                self.boundrate = self.config[SerialRef.SERIAL.value][SerialRef.BOUNDRATE.value]
                self.boot_time = self.config[SerialRef.SERIAL.value][SerialRef.BOOT_TIME.value]
                self.orin_scale = self.config[UnitRef.UNITS.value][UnitRef.ORIN_SCALE.value]
                self.acel_scale = self.config[UnitRef.UNITS.value][UnitRef.ACEL_SCALE.value]
                self.gyro_scale = self.config[UnitRef.UNITS.value][UnitRef.GYRO_SCALE.value]
        except:
            print("[WARN]: No config file. Setting defalut variables")

        try:
            self.ser_ = serial.Serial(port=self.port, baudrate=self.boundrate, timeout=1)
            print("[INFO]: Connection: OK")
            self.ser_.write((GeneralCmdRef.STOP_POST.value).encode(EncodingFormat.UTF_8.value))

            # Flushing output
            discard = self.ser_.readline() 

            if self.has_config:
                ConfigWriter(self.ser_, self.config)

            self.ser_.write((GeneralCmdRef.OUTPUT_FORMAT.value).encode(EncodingFormat.UTF_8.value))
            self.ser_.write((GeneralCmdRef.START_POST.value).encode(EncodingFormat.UTF_8.value))   

            self.mainThread = threading.Thread(target=self.update)
            time.sleep(self.boot_time)
        except:
            print("[ERRO]: Couldn't connect to Serial")
            self.mainThread = threading.Thread(target=lambda: print("[WARN]: Serial not connected!"))
         
    def update(self):
        while(self.on):
            self.poll()
    
    def poll(self):
        try:
            line = bytearray(self.ser_.readline()).decode(EncodingFormat.UTF_8.value)
            line = line.split('=')[1]
            values = [float(val) for val in line.split(',')]
            
            # Converts to rad
            self.orient['x'] = values[0] * self.orin_scale
            self.orient['y'] = values[1] * self.orin_scale
            self.orient['z'] = values[2] * self.orin_scale

            # Converts to m/s^2
            self.accel['x'] = values[3] * self.acel_scale
            self.accel['y'] = values[4] * self.acel_scale
            self.accel['z'] = values[5] * self.acel_scale

            # Converst to rad/s
            self.gyro['x'] = values[6] * self.gyro_scale
            self.gyro['y'] = values[7] * self.gyro_scale
            self.gyro['z'] = values[8] * self.gyro_scale
        except:
            print("[WARN]: Can't read data")
    
    def run_thread(self):
        return self.accel['x'], self.accel['y'], self.accel['z'], self.gyro['x'], self.gyro['y'], self.gyro['z'], self.temp
    
    def run(self):
        self.poll()
        return self.run_thread()

    def start(self):
        if not self.on:
            self.on = True
            self.mainThread.start()
        else:
            print("[WARN]: IMU already ON!")
    
    def shutdown(self):
        self.on = False
        self.mainThread.join()


# EXAMPLE
# Just and example of how RazorIMU can be used
# Remove that method during actuall implimentation

if __name__ == "__main__":
    razor_imu = RazorIMU('razor.yaml')
    razor_imu.start()
    time.sleep(2)
    for t in range(1,20):
        print(str(razor_imu.accel['x']))
        time.sleep(0.2)
    razor_imu.shutdown()
    print("All Good!")