
import time
import serial
import yaml
import threading

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BOUNDRATE = 57600

class RazorIMU():
    def __init__(self, config_path=None):
        self.on = False
        self.has_config = False
        self.config = None
        self.port = DEFAULT_PORT
        self.boundrate = DEFAULT_BOUNDRATE

        try:
            with open(config_path, "r") as yamlfile:
                data = yaml.load(yamlfile, Loader=yaml.FullLoader)
                print("[INFO]: Got config file!")
                self.has_config = True
                self.config = data
        except:
            print("[WARN]: No config file. Setting defalut variables")

        self.accel = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.gyro = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.mag = {'x': 0., 'y': 0., 'z': 0.}
        self.temp = None

        try:
            self.ser_ = serial.Serial(port=self.port, baudrate=self.boundrate, timeout=1)
            print("[INFO]: Connection: OK")
            self.ser_.write(('#o0').encode("utf-8"))
            discard = self.ser_.readline() # Flushing output

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
            self.ser_.write(('#o1').encode("utf-8"))   
            print("[INFO]: Good to go!")
            self.mainThread = threading.Thread(target=self.update)
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
            self.accel = { 'x' : values[3], 'y' : values[4], 'z' : values[5]}
            self.gyro = { 'x' : values[6], 'y' : values[7], 'z' : values[8]}
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

    
if __name__ == "__main__":
    razor_imu = RazorIMU('razor.yaml')
    razor_imu.start()
    time.sleep(5)
    print(str(razor_imu.accel['x']))
    razor_imu.shutdown()
    print("All Good!")