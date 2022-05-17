#ifndef SERIAL
#define SERIAL



/*Initialising the baud rate for the serial interface*/
void initSerial_SCI1(void);

/*Sending data through the serial interface*/
void sendData(char data);

/*Breaking apart struct data into single chars to be sent*/
void outputSerial_SCI1(char *data, int length);


struct MSG_HEADER {
   int sentinel;
   char msg_type[8];
   unsigned int msg_size;
   unsigned int header_time;
   int end_sentinel;
}

struct DATA {
    int first_sentinal;
    int angle_azimuth;
    int angle_elevation;
    unsigned int range;
    int final_sentinal;
}

#endif