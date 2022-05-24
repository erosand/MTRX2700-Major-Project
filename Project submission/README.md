# MTRX2700-Major-Project- Sexy Scanner 3000
## The Problem
For a supermarket to bring products to shelves, a large degree of unseen product movement and management occurs behind the scenes. The products received from the production point are often stored in intermediary warehouses, stepping down from a handful of huge national houses to smaller local warehouses outside of the city. From there, stock is moved from supermarket back of house storages and finally to the shelves. Stock in these areas are generally stored in bulk, depending on the product type usually either in large cardboard boxes or plastic wrapped. A problem we identified in this process was in the managing and quantifying of stock in these huge warehouses, where stock boxes often look nearly identical and visually checking is rarely efficient.

## Our Solution
Our solution, the Sexy Scanner 3000, aims to automate scanning of shelves to detect stock boxes. These scanner modules are either placed on warehouse shelves, facing the stock, or ceiling mounted, face-down at a grid of stacked boxes. By utilising the PTU servos and liDAR, it scans a depth field in a pyramid like field of view. From this, a point cloud of the stock was produced, and analysed using a DFS search algorithm. This algorithm was used to determine how many boxes are present by calculating the height of stacks of boxes. This works under the assumption that at one time, it is scanning boxes of the same type and dimensions, but parameters of our software can be easily changed to detect different stock types, and from further distances. 
This was demonstrated at a small scale by propping the PTU on a small ladder and scanning a stack of small cube boxes.

## Summary
Keeping track of stock status in a storage using a lidar mounted in the ceiling (or on a shelf.
The lidar is mounted above the storage area, minimum and maximum range for the scanner are specified, and scanning is started. The measurements form a point cloud, which is refined to identify the top sides of each individual box. The scans are repeated with a desired time interval, and any changes in between scans can alert the user that it's time to restock.

## Modules:

### Controlling LIDAR orientation
Output: Current orientation(two angles in integer degrees)
The servo moves in a snaked pattern, taking measurements at 1 degree increments azimuthally before incrementing its elevation. 
These measurements were manually scaled from the input PWM signals.

### LIDAR sensor info to distance
Output: Distance data (millimetres) at an address (type long int)
The LIDAR sensor continuously sends a PWM signal to port 1 of the timer module. The timer channel 1 is set up to input capture and records the timer count at each rising and falling edge of the PWM signal. At each falling edge an interrupt service routine calculates the period of the PWM and stores this in memory. At each iteration of the main for(;;) loop the raw LIDAR data is scaled to mm and stored in an integer variable singleSample. 

### Serial Communication
Input: 3 integers representing point data for azimuth, elevation and scaled lidar reading
Output: A comma separated string is sent to the serial port
The data is stored in a buffer in a predetermined format of “Point, {elevation}, {azimuth}, {lidarSample}\n” and this was sent to the serial port for each angle iteration. It is sent out using SerialOutputChar and SerialOutputString, which iterates through the string and sends the data out character by character. This module was tested by visually examining the sent data via the putty terminal before attempting to communicate with the visual plotting module. This was possible because all data was sent as ASCII characters, which are human-readable.

### Data unpacking and Visual Interface
Input: A struct containing distance, elevation and azimuth for a point in the point cloud.
Output: 3 dimensional point cloud
The interface received serial data and first converted each data point into x,y,z values using trigonometric operations. Before scanning, parameters are defined for the acceptable bounds of scanning (generally the distance from the lidar to the ground), and outliers outside of these bounds are discarded. After a predetermined number of points are collected(e.g. 10000), the python matplotlib.pyplot module is used to plot a 3D point cloud

### DFS Box counting Algorithm (unintegrated with rest of code, but working with sample data)
Input: a 2D array of points with corresponding depth values
Output: an integer number of boxes
From the point cloud data/simulated data a DFS search is conducted before points which are within close proximity are clustered. From each cluster, its height is compared to the manually set or calibrated size of an actual box, and this is used to count the number of boxes in each stack. The number of these boxes is summed up and printed to the python terminal, representing a visual interface for supermarkets to track several of these modules situated around their warehouses.



