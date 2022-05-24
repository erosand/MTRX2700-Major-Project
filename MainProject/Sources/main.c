#include <hidef.h>      /* common defines and macros */
#include <assert.h>
#include "derivative.h"      /* derivative-specific definitions */

// need this for string functions
#include <stdio.h>

#include "pll.h"
#include "serial.h"

#include "l3g4200d.h"

#include "servo.h"
#include "laser.h"

#include "gyro.h"


void printErrorCode(IIC_ERRORS error_code) {
  struct MSG_HEADER error_header; //this is a different header from what is used in main
  char error_buffer[128]; //this is a buffer to store the ASCII string chars   
  switch (error_code) {
    case NO_ERROR:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 16;
      sprintf(error_buffer, "IIC: No error\r\n");
      break;
    
    case NO_RESPONSE:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 19; 
      sprintf(error_buffer, "IIC: No response\r\n");
      break;
    
    case NAK_RESPONSE:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 22;
      sprintf(error_buffer, "IIC: No acknowledge\r\n");
      break;
    
    case IIB_CLEAR_TIMEOUT:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 33;
      sprintf(error_buffer, "IIC: Timeout waiting for reply\r\n");
      break;
    
    case IIB_SET_TIMEOUT: 
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 23;
      sprintf(error_buffer, "IIC: Timeout not set\r\n");
      break;
    
    case RECEIVE_TIMEOUT:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 24;
      sprintf(error_buffer, "IIC: Received timeout\r\n");
      break;
    
    case IIC_DATA_SIZE_TOO_SMALL:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 27;
      sprintf(error_buffer, "IIC: Data size incorrect\r\n");
      break;

    default:
      strcpy(error_header.msg_type, "text");
      error_header.msg_size = 21;
      sprintf(error_buffer, "IIC: Unknown error\r\n");
      break;
  }
  outputSerial_SCI1((char*)&error_header, sizeof(error_header)); 
  outputSerial_SCI1((char*)&error_buffer, error_header.msg_size);
}

void main(void) {
  
  ////////      DEFINITIONS       ////////
  
  //sensor variables
  AccelRaw read_accel;
  AccelScaled scaled_accel;
  GyroRaw read_gyro;
  unsigned long laserSample;
  struct MSG_HEADER header;
  struct DATA sensor_values;//a place to collect all the sensor data into
  
  //error code variable
  IIC_ERRORS error_code = NO_ERROR;
  
  //serialisation variables
  
  header.sentinel = 0xABCD;
  strcpy(&header.msg_type,"point");
  header.msg_size = sizeof(struct DATA); 
  header.end_sentinel = 0xDCBA;
  sensor_values.first_sentinal = 0xAAAA;
  sensor_values.final_sentinal = 0xBBBB;
  
  
  //assert(error_code != NO_ERROR);


  ////////    INITIALISATIONS     ////////
  
  PLL_Init(); // makes sure the board is set to 24MHz. this is needed only when not using the debugger
  PWMinitialise();
  setServoPose(100, 100);
  initSerial_SCI1();
  
  error_code = iicSensorInit();   // initialise the sensor suite
  // write the result of the sensor initialisation to the serial
  printErrorCode(error_code);

  laserInit();//initialise timer module to measure LIDAR pulse width     
  Init_TC6();//initialise timer module to trigger regular interupts to move the servos
  
  
  //////     ENTER MAIN LOOP       //////
	EnableInterrupts;
  //COPCTL = 7;
  _DISABLE_COP();
    
  for(;;) {
  
    // read the gyro raw value
 /*   error_code = getRawDataGyro(&read_gyro);   
    if (error_code != NO_ERROR) {
      printErrorCode(error_code);    
      error_code = iicSensorInit();
      printErrorCode(error_code);  
      continue; 
    }
    
    //read the accelerometer raw value
    error_code = getRawDataAccel(&read_accel);
    if (error_code != NO_ERROR) {
      printErrorCode(error_code);   
      error_code = iicSensorInit();
      printErrorCode(error_code); 
      continue; 
    }    */
    
    //read the scaled(in mm) LIDAR range value    
    GetLatestLaserSample(&laserSample);

    // convert the acceleration to a scaled value
    convertAccelUnits(&read_accel, &scaled_accel);
    
    //convert the gyroscope to a scaled value
    //this might be a function where we also integrate angular velocity collected from the gyro
        
    
    // collecting all the sensor values is now done
    // Now we need to fill in the struct DATA sensor_values with the appropriate numbers to be sent over serial
    sensor_values.angle_azimuth = 0;  //just temporary 
    sensor_values.angle_elevation = scaled_accel.z; //this needs to be converted to an angle. Only temporary 
    sensor_values.range = laserSample;
    
    // first send the header
    outputSerial_SCI1((char*)&header, sizeof(struct MSG_HEADER));
    //then send the data that follows the header
    outputSerial_SCI1((char*)&sensor_values, sizeof(struct DATA));
    
    //_FEED_COP(); /* feeds the dog */
  } /* loop forever */
  
  /* please make sure that you never leave main */
}

