# MTRX2700-Major-Project

Modules:

User interface - Erik
Input: Distance, elevation and azimuth for a point in the point cloud.
Output: Fancy plots

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
