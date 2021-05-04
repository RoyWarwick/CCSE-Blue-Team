/**********************************************************************
Program adapted from www.freenove.com
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

signed main(int argc, char * argv[]) {
    char key = 0;
    wiringPiSetup();
	keypad.setDebounceTime(50);	
	pinMode(26, OUTPUT); // Blue LED
    while (1) {
        key = keypad.getKey();  //get the state of keys
        if (key) {// when a key is pressed
            delay(10);
            if (digitalRead(26) == HIGH)
                printf("OK: Key pressed and the blue LED turned on.\n");
            else
                printf("ERROR: Key pressed and the blue LED did not turn on.\n");
        }
    }
}
