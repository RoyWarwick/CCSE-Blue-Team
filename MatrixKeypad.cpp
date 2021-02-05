/**********************************************************************
* Filename    : MatrixKeypad.cpp
* Description : Obtain the key code of 4x4 Matrix Keypad
* Author      : www.freenove.com
* modification: 2019/12/27
**********************************************************************/
#include "Keypad.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#include <string.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
char keys[ROWS][COLS] = {  //key code
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};

byte rowPins[ROWS] = {1, 4, 5, 6}; //define the row pins for the keypad
byte colPins[COLS] = {12, 3, 2, 0}; //define the column pins for the keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS); //create Keypad object

signed main(void) {
    wiringPiSetup();
    char key = 0;
	keypad.setDebounceTime(50);
	
	pinMode(26, OUTPUT); // Blue LED
	char hold[4], i = 17;
	char cmd[] = "test -z \"$(grep \"xxxx\" PINs)\"";
	char send[] = "mosquitto_pub -t security -m \"xxxxxxxxxx xxxxxx\"";
    while (1) {
        key = keypad.getKey();  //get the state of keys
        if (key) {// when a key is pressed
            if (key == '#' || key == '*') {
                if (i < 21) {
                    // Error - too short
                    digitalWrite(26,HIGH);
                    delay(200);
                	digitalWrite(26,LOW);
                	delay(200);
                	digitalWrite(26,HIGH);
                    delay(200);
                	digitalWrite(26,LOW);
                } else {
                    sprintf(send+30,"%d",(unsigned long)time(NULL));
                    send[40] = ' ';
                    send[41] = cmd[17];
                    send[42] = cmd[18];
                    send[43] = cmd[19];
                    send[44] = cmd[20];
                    send[45] = key;
                    // Find string
                    if (system(cmd) == 0) {
                        send[46] = 'F';
                    	system(send);
                        digitalWrite(26,HIGH);
                        delay(200);
                    	digitalWrite(26,LOW);
                    	delay(200);
                    	digitalWrite(26,HIGH);
                        delay(200);
                    	digitalWrite(26,LOW);
                    	i = 17;

                    } else {
                        //success
                        system("killall alarm 2> /dev/null");
                        system("./off");
                        send[46] = 'T';
                    	system(send);
                        digitalWrite(26,HIGH);
                        delay(500);
                    	digitalWrite(26,LOW);

                    }
                }
                i = 17;
            } else if (i == 21) {
                i = 17;
                // Error - too long
                digitalWrite(26,HIGH);
                delay(200);
            	digitalWrite(26,LOW);
            	delay(200);
            	digitalWrite(26,HIGH);
                delay(200);
            	digitalWrite(26,LOW);
            } else {
                digitalWrite(26,HIGH);
                delay(10);
            	digitalWrite(26,LOW);
            	delay(10);
                cmd[i] = key;
        	    i++;
    	    }
        }
    }
}
