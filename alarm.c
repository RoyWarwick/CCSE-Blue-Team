#include <wiringPi.h>
#include <stdio.h>

signed main(void) {
    wiringPiSetup();
	pinMode(23, OUTPUT); //Red LED
	pinMode(24, OUTPUT); //Red LED
	while (1) {
    	digitalWrite(23,HIGH);
    	digitalWrite(24,LOW);
    	delay(500);
    	digitalWrite(23,LOW);
    	digitalWrite(24,HIGH);
    	delay(500);
	}
}

//29
