# MTRX2700-Major-Project

Modules:

User interface - Erik
Input: Stock status (an integer, which in binary has one bit for each spot on the shelf)
Output: Fancy plots, possibly commands from the user?

LIDAR sensor info to distance - Ivo
Output: Distance data (meters) at an address (type float)

Controlling LIDAR orientation - Lincoln
Input: Desired orientation(two angles at memory address (float)), current orientation

Checking LIDAR orientation using IMU - Lincoln
Input: IMU data (from I2C)
Output: Orientation (angle in degrees?)

Logic for LIDAR movement - Jonathan and Jackson
Input: Current orientation, status?
Output: New desired LIDAR orientation
