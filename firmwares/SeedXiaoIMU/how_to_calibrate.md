# Axis Constant Drift

Upload firmware to the Seeed XIAO board, boot it and leave it in stale position.
Enable prints out and let it run for 40-80 loops and stop it.

Count number of outputs and initial and final values of each axis.

Ex.
  ```serial
  20:11:54.916 -> #YPRAG=54.97,203.44,286.21,-0.00,-1.00,0.17,0.91,-1.96,-0.42
  20:11:54.916 -> #YPRAG=54.97,203.45,286.21,-0.00,-1.00,0.17,0.98,-2.38,-0.21
  20:11:54.949 -> #YPRAG=54.97,203.45,286.22,0.00,-1.00,0.17,0.91,-2.10,-0.14
  20:11:54.980 -> #YPRAG=54.96,203.46,286.22,-0.00,-1.00,0.17,0.91,-2.17,-0.28
  20:11:55.013 -> #YPRAG=54.97,203.47,286.23,-0.00,-1.00,0.17,0.98,-2.24,-0.21
  20:11:55.044 -> #YPRAG=54.97,203.48,286.24,-0.00,-1.00,0.17,0.91,-2.24,-0.14
  20:11:55.044 -> #YPRAG=54.97,203.48,286.25,-0.00,-1.00,0.17,0.91,-2.45,-0.07
  20:11:55.076 -> #YPRAG=54.97,203.49,286.26,-0.00,-0.99,0.18,0.84,-2.17,-0.14
  ```

  Here we have `8` **iterations** and `first/last` values for: 
  - `X`: `54.97/54.97`
  - `Y`: `203.44/203.49`
  - `Z`: `286.21/286.21`

Then to find `AXIS_DRIFT` for each axis calculate $drift = \frac{final-initial}{iterations}$.
Repeat for every axis. 

Write down resulting value in configuration `.yaml` file.

# Axis Scaling

Upload firmware to the Seeed XIAO board, boot it and leave it in stale position.
Record initial value of axis, and rotate device over the axis for exactly 90 deg. (Or what ever units you prefere). This is our **desired angle**.

Record resulting value on that axis. This is our **actual angle**.
Then to find `AXIS_SCALE` for each axis calculate $scale = \frac{desired_angle}{actual_angle}$.
Repeat for every axis. 

Write down resulting value in configuration `.yaml` file.




