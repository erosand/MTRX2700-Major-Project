#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */

void timerSetupPulseWidth(void);


// Global variables
int pulseHigh;
uint_16 count_current;
uint_16 count_revious;

void main(void) {
  /* put your own code here */
  
  
  
  
  
  


	EnableInterrupts;


  for(;;) {
    _FEED_COP(); /* feeds the dog */
  } /* loop forever */
  /* please make sure that you never leave main */
}

void timerSetupPulseWidth() {
  TSCR2 = TSCR2 | 4;  // Set prescaler to 16  (maximum pusle width that can be measured is 43.6ms)
  // Channel 1 is already in input capture mode
  TCTL = // Set channel 1 to capture input on falling AND rising edges
  pulseHigh = 0;
  count_current = 0;
  count_previous = 0;
  TIE = 2;        // Channel 1 can trigger interrupts
  TSCR1_TEN = 1;  // Enable timer
}

interrupt 9 void TC5_isr() {
  TFLG1 = TFLG1 & 0b00000010; //clear C0F in TFLG1
  count_current = TC5;
  pulseHight = //toggle pusleHigh.  
  
}
