#include <wiringPi.h>
#include <stdio.h>

signed main(void) {
    wiringPiSetup();
    pinMode(22,INPUT);
    pinMode(23, OUTPUT); //Red LED
    pinMode(24, OUTPUT); //Red LED
    while (1) {
        while (digitalRead(22) != HIGH);
        delay(100);
        if (digitalRead(23) == HIGH || digitalRead(24) == HIGH)
            printf("OK: Sensor activated and alarm started.\n");
        else
            printf("ERROR: Sensor activated but alarm not started.\n");
    }
}
