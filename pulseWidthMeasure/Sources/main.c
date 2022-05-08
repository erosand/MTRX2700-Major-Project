#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */



void timerLidarSetup(void);
float getLidarRange(void);



// Global variables
uint_8  pulseHigh;
uint_16 count_current;
uint_16 count_previous;



void main(void) {
  /* put your own code here */
	EnableInterrupts;

  for(;;) {
    _FEED_COP(); /* feeds the dog */
  } /* loop forever */
  /* please make sure that you never leave main */
}



void timerLidarSetup() {
  TSCR2 = TSCR2 | 4;  // Set prescaler to 16  (maximum pusle width that can be measured is 43.6ms)
  // Channel 1 is already in input capture mode
  TCTL = // Set channel 1 to capture input on falling AND rising edges
  pulseHigh = 0;
  count_current = 0;
  count_previous = 0;
  TIE = 2;        // Channel 1 can trigger interrupts
  TSCR1_TEN = 1;  // Enable timer
}



float getLidarRange(void) {
  return (float)timer_dif * (24000000/16);//16 is the prescaler value. 24000000 is CPU clock frequency  
}



interrupt 9 void TC5_isr() {
  TFLG1 = TFLG1 & 0b00000010; //clear C0F in TFLG1
  count_current = TC1;
  pulseHigh = pulseHigh ^ 0b1;  //toggle pusleHigh.
  
  if (pulseHigh == 0) { //falling edge occurred
    if (TFLG2) { //if timer overflowed
      time_dif = (1<<16) - count_previous + count_current;
      TFLG2 = 128;  //clearing TOF
    }
    else {       //timer did not overflow
      time_dif = count_current - count_previous;  
    }
  }
  
  if (pulseHigh == 1) { //rising edge occurred 
    count_previous = count_current; //prepare for next interrupt  
  }
}
