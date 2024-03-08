
import math
import time
import serial
import yaml
import threading

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
                self.port = self.config['Serial']['port']
                self.boundrate = self.config['Serial']['boundrate']
                self.boot_time = self.config['Serial']['boot_time']
        except:
            print("[WARN]: No config file. Setting defalut variables")

        try:
            self.ser_ = serial.Serial(port=self.port, baudrate=self.boundrate, timeout=1)
            print("[INFO]: Connection: OK")
            self.ser_.write(('#o0').encode("utf-8"))

            # Flushing output
            discard = self.ser_.readline() 

            self.ser_.write(('#ox').encode("utf-8"))
            if self.has_config:
                print("[INFO]: Writing calibration data...")
                self.ser_.write(('#caxm' + str(self.config['Calib']['accel_x_min'])).encode("utf-8"))
                self.ser_.write(('#caxM' + str(self.config['Calib']['accel_x_max'])).encode("utf-8"))
                self.ser_.write(('#caym' + str(self.config['Calib']['accel_y_min'])).encode("utf-8"))
                self.ser_.write(('#cayM' + str(self.config['Calib']['accel_y_max'])).encode("utf-8"))
                self.ser_.write(('#cazm' + str(self.config['Calib']['accel_z_min'])).encode("utf-8"))
                self.ser_.write(('#cazM' + str(self.config['Calib']['accel_z_max'])).encode("utf-8"))

                self.ser_.write(('#cmxm' + str(self.config['Calib']['magn_x_min'])).encode("utf-8"))
                self.ser_.write(('#cmxM' + str(self.config['Calib']['magn_x_max'])).encode("utf-8"))
                self.ser_.write(('#cmym' + str(self.config['Calib']['magn_y_min'])).encode("utf-8"))
                self.ser_.write(('#cmyM' + str(self.config['Calib']['magn_y_max'])).encode("utf-8"))
                self.ser_.write(('#cmzm' + str(self.config['Calib']['magn_z_min'])).encode("utf-8"))
                self.ser_.write(('#cmzM' + str(self.config['Calib']['magn_z_max'])).encode("utf-8"))
        
                self.ser_.write(('#cgx' + str(self.config['Calib']['gyro_average_offset_x'])).encode("utf-8"))
                self.ser_.write(('#cgy' + str(self.config['Calib']['gyro_average_offset_y'])).encode("utf-8"))
                self.ser_.write(('#cgz' + str(self.config['Calib']['gyro_average_offset_z'])).encode("utf-8"))

                self.orientC = self.config['Units']['orin_scale']
                self.accelC = self.config['Units']['acel_scale']
                self.gyroC = self.config['Units']['gyro_scale']

            self.ser_.write(('#o1').encode("utf-8"))   
            print("[INFO]: Good to go!")
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
            line = bytearray(self.ser_.readline()).decode("utf-8")
            line = line.split('=')[1]
            values = [float(val) for val in line.split(',')]
            
            # Converts to rad
            self.orient['x'] = values[0] * self.orientC
            self.orient['y'] = values[1] * self.orientC
            self.orient['z'] = values[2] * self.orientC

            # Converts to m/s^2
            self.accel['x'] = values[3] * self.accelC
            self.accel['y'] = values[4] * self.accelC
            self.accel['z'] = values[5] * self.accelC

            # Converst to rad/s
            self.gyro['x'] = values[6] * self.gyroC
            self.gyro['y'] = values[7] * self.gyroC
            self.gyro['z'] = values[8] * self.gyroC
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