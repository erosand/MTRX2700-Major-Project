# MTRX2700-Major-Project

Project overview:

Keeping track of stock status in a storage using a lidar mounted in the ceiling.


Modules:


User interface - Erik

Input: Serial data containing distance, elevation and azimuth for a point in the point cloud.

Output: 3D plot of the point cloud, list of all points.


LIDAR sensor info to distance - Ivo

Output: Distance data (millimeters) at an address (type int)

 
LIDAR movement - Lincoln 

Input: Current orientation (two angles at memory address, type int)

Output: New desired LIDAR orientation, commands to actuators


Post-processing of the point cloud - Jonathan

Input: List of points in point cloud

Output: Refined plot of storage status


Serialisation - Jackson 

Input: Sensor data in memory

Output: Serial data sent to python


