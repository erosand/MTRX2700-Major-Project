#include "serial.h"
#include <mc9s12dp256.h>



void initSerial_SCI1(void){
    //Setting Baud rate to 9600 (default)
    SCI1BDL = 0x9C;
    SCI1BDH = 0;        
    
    SCI1CR1 = 0x00;
    SCI1CR2 = 0x0C;
} 


void sendData(char data) {
    while (!(SCI1SR1 & 0x80));
    SCI1DRL = data;     
}


//int length is the number of bytes(chars) to send
void outputSerial_SCI1(char *data, int length) {
    int i = 0;
    for (i = 0; i < length; i++) {
        sendData(*data);
        data++;    
    }
    
}


