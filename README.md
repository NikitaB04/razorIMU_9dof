# razorIMU_9dof

Python RazorIMU class designed for reading data via Serial communication, with any board mimicking [SparkFun 9DoF Razor](https://learn.sparkfun.com/tutorials/9dof-razor-imu-m0-hookup-guide/all) communication format.

---

## Methods
`RazorIMU( [config_path] )` - Constructor for RazorIMU, configures board and writes calibration values provided in `config_path.yaml` file.
`start()` - starts polling the data from Serial, can call as soon as created RazorIMU object.
`shutdown()` - stops the polling, not mendatory, but please shutdown the IMU when done. 
`run_thread()` - returns most recent recived data from IMU in as a list `[accel.x, accel.y, accel.z, gyro.x, gyro.y, gyro.z, temp]`.
\* *No need to use any other methods, those are enough for full use, see example code in in `__main__` section at bottom of `imu.py`*

---

## Features
- Multithreading on update.
- Reading config files (example attached).
- Writing callibration values.

---

## TODO
- Unit conversions.
- Test implementation.
- Test calibration writing.

---

## Notes
Currently class doesn't apply any conversion to the values, so it gives RAW DATA (aka. gravity is around -250 $units/s^2$).
Also be carreffuly after calling `start()` with interval of few seconds after creating `RazorIMU` object, Due to the way how serial read works, `tty*` might build up ~8k of data over the interval betwenn construction and start of the thread.
It shouldn't cause any issues, since dumping will be automatic and as quick as your executing device lets it, and as soon as it catches up with current data will work as intended. 
