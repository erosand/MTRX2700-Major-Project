#ifndef __laser_h
#define __laser_h

// get the latest laser measurement
unsigned long GetLatestLaserSample(void);


// initialise the laser timer
void laserInit(void);


// interrupt for reading the laser signal
__interrupt void TC1_ISR(void);

#endif