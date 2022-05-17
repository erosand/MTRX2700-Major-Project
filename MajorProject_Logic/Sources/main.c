#include <hidef.h>      /* common defines and macros */
#include <stdio.h>
#include "serial.h"
#include "derivative.h"      /* derivative-specific definitions */




struct DATA {
    int first_sentinal;
    int angle_horizontal;
    int angle_vertical;
    unsigned int length;
    int final_sentinal;
};


void main(void) {
    /* put your own code here */
    struct DATA data = {0xAA, 10, 90, 10000, 0xBB};
    
    initSerial();
    serialisingData((char*)&data, sizeof(struct DATA));



	EnableInterrupts;


    for(;;) {
    
    } 
}
