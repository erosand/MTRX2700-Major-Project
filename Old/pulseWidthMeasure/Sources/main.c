#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */
#define FULL_TIMER 65535


void timerLidarSetup(void);
float getLidarRange(void);
interrupt 9 void TC1_ISR(void);



// Global variables
//uint8_t  pulseHigh;
//uint_16 count_current;
//uint_16 count_previous;
unsigned long timer_dif;
unsigned char pulseHigh;
unsigned int count_current;
unsigned int count_previous;


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
  TCTL4 = TCTL4 & 0b1100;// Set channel 1 to capture input on falling AND rising edges
  pulseHigh = 0;
  count_current = 0;
  count_previous = 0;
  TIE = 2;        // Channel 1 can trigger interrupts
  TSCR1_TEN = 1;  // Enable timer
}



// returns range in units of metres.
float getLidarRange(void) {
  return (float)1000 * timer_dif * (24000000/16);//16 is the prescaler value. 24000000 is CPU clock frequency  
}



#pragma CODE_SEG __NEAR_SEG NON_BANKED /* Interrupt section for this module. Placement will be in NON_BANKED area. */
__interrupt 9 void TC1_ISR() {
  count_current = TC1;
  pulseHigh = pulseHigh ^ 0b1;  //toggle pusleHigh.
  
  if (pulseHigh == 0) { //falling edge occurred
    if (TFLG2) { //if timer overflowed
      timer_dif =  FULL_TIMER - count_previous + count_current;
      TFLG2 = 128;  //clearing TOF
    }
    else {       //timer did not overflow
      timer_dif = count_current - count_previous;  
    }
  }
  
  if (pulseHigh == 1) { //rising edge occurred 
    count_previous = count_current; //prepare for next interrupt  
  }
  
  TFLG1 = TFLG1 & 0b00000010; //clear C1F in TFLG1
}
