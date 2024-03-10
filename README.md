# razorIMU_9dof

Python RazorIMU class designed for reading data via Serial communication, with any board mimicking [SparkFun 9DoF Razor](https://learn.sparkfun.com/tutorials/9dof-razor-imu-m0-hookup-guide/all) communication format.

---

## Methods
`RazorIMU( [config_path] )` - Constructor for RazorIMU, configures board and writes calibration values provided in `config_path.yaml` file.

`start()` - starts polling the data from Serial, can call as soon as created RazorIMU object.

`shutdown()` - stops the polling, not mendatory, but please shutdown the IMU when done. 

\* *No need to use any other methods, those are enough for full use, see example code in in `__main__` section at bottom of `imu.py`*

---

## Data
`orient[<axis>]` - angular orientation of device across `<axis>` in $rad$

`accel[<axis>]` - linear acceleratio across `<axis>` in $m/s^2$

`gyro[<axis>]` - angular velocity across `<axis>` in $rad/s$

---

## Configuration File
Overview of how to properly setup a configuration file.

#### Serial
`device` - name of device to be connected, must match with `Calib` name for proper execution of calibration commands.

`port` - path to serial to which device is connected (ex. `/dev/ttyUSB0`).

`boundrate` - boundrate of device.

`boot_time` - amount of time before device execution starts after boot beyond regular boot time, extra to ensure proper load of calibration values.

#### Units
`orin_scale/acel_scale/gyro_scale` - unit conversion constant, in case if firmware uses differnt units from expected.

#### Calib
A section which defines set of commands to set up calibration parameters to device and it's values.
Follow the template to create your own calibration sequence for device:

```yaml
DEVICE_NAME:
  Val:
    value1: [value to be written]
    value2: [value to be written]
    value3: [value to be written]
  Cmd:
    value1: [serial command used to write value1]
    value2: [serial command used to write value2]
    value3: [serial command used to write value3]

```

\* *Ensure that `DEVICE_NAME` mathes `Serial.device` value, so alibration will use specified calibration sequence.*


\* *Ensure that `Val.[your_varible]` and `Cmd.[your_varible]` have same `[your_varible]` name, for propper mapping of commands to written values.*

---

## Firmwares
Folder `firmwares` should include some common of the IMU sensors avaliable.

---

## TODO
- SeeedXIAO calibration commands

---

## Notes
Be carreffuly after calling `start()` with interval of few seconds after creating `RazorIMU` object, Due to the way how serial read works, `tty*` might build up ~8k of data over the interval betwenn construction and start of the thread.
It shouldn't cause any issues, since dumping will be automatic and as quick as your executing device lets it, and as soon as it catches up with current data will work as intended. 
