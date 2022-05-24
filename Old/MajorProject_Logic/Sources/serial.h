#ifndef SERIAL
#define SERIAL



/*Initialising the baud rate for the serial interface*/
void initSerial(void);

/*Sending data through the serial interface*/
void sendData(char data);

/*Breaking apart struct data into single chars to be sent*/
void serialisingData(char *data, int length);


#endif