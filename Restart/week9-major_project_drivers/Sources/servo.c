
#include "derivative.h"
#include <math.h> 
#include "servo.h"


#define ZERO_ELEVATION_DUTY 4600
#define ZERO_AZIMUTH_DUTY 2000


void PWMinitialise(void){
    // set PP5 and PP7 for pwm output 
    PWMCLK = 0; // select clock A
    PWMPOL = 0xA0; // PWM5 and PWM7 output start high
    PWMCTL = 0xC0; // 16-bit PWM: use PWM4 and PWM5 for PWM5, PWM6 and PWM7 for PWM7
    PWMCAE = 0; // Center aligned
    PWMPRCLK = 0x33; // PWM Clock prescaler to 8 

    // set the PWM period appropriate for servos
    PWMPER45 = 0xEA6A;
    PWMPER67 = 0xEA6A;

    // set the initial duty cycle for both servos
    PWMDTY45 = ZERO_ELEVATION_DUTY;
    PWMDTY67 = ZERO_AZIMUTH_DUTY;
    
    PWME  |= 0xFF;      // enable PWM0
}

void setServoPose(int azimuth, int elevation){  
    PWMDTY45 = (int)(ZERO_ELEVATION_DUTY + elevation);  // Sets elevation to duty cycle using PWM 45
    PWMDTY67 = (int)(ZERO_AZIMUTH_DUTY + azimuth);   // Sets azimuth to duty cycle using PWM 67
}


void Init_TC6 (void) {
  TSCR1_TEN = 1;
  
  TSCR2 = 0x00;   // prescaler 1, before 32 = 0x04
  TIOS_IOS6 = 1;   // set channel 6 to output compare
    
  TCTL1_OL6 = 1;    // Output mode for ch6
  TIE_C6I = 1;   // enable interrupt for channel 6

  TFLG1 |= TFLG1_C6F_MASK;
}


// variables to make the servo move back and forth
// note: This is just to demonstrate the function of the servo
long iter_azimuth = 0;
long iter_elevation = 0;
int toggle = 0;
int toggle_elev = 0;
int theta_azimuth = 20;
int theta_elevation = 20;
int theta_step = 30;




// the interrupt for timer 6 which is used for cycling the servo
#pragma CODE_SEG __NEAR_SEG NON_BANKED /* Interrupt section for this module. Placement will be in NON_BANKED area. */
__interrupt void TC6_ISR(void) { 
    
  
  TC6 = TCNT + 64000;   // interrupt delay depends on the prescaler
  TFLG1 |= TFLG1_C6F_MASK;
  servoMove( &current_elevation, &current_azimuth);

  
  
}


void servoMove(int* elevation, int*azimuth){
  if(toggle == 0){
    iter_azimuth++;
  }else{
     iter_azimuth--;
  }
  if (iter_azimuth > theta_azimuth*theta_step| iter_azimuth < -1*theta_azimuth*theta_step) {
    toggle = ~toggle;
  
    if (toggle_elev == 0) 
      iter_elevation += 1*theta_step;
    else 
      iter_elevation -= 1*theta_step;
    
    
    if (iter_elevation > theta_elevation*theta_step|iter_elevation < -1*theta_elevation*theta_step){
      
      toggle_elev = ~toggle_elev;
    }
  }
    
  setServoPose(2700 + iter_azimuth, iter_elevation); 
  *elevation = (int)iter_elevation/theta_step;   
  *azimuth = (int)iter_azimuth/theta_step;
}
  