#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>

signed main(void) {
    char send[] = "mosquitto_pub -t security -m \"xxxxxxxxxx x\"";
    wiringPiSetup();
    pinMode(22,INPUT);
    
    while (1) {
        if (digitalRead(22) == HIGH) {
	        if (system("test -z \"$(pgrep alarm)\"") == 0)
                system("/usr/security/alarm &");
            sprintf(send+30,"%d",(unsigned long)time(NULL));
            send[40] = ' ';
            send[41] = 'A';
            system(send);
            delay(2000);
        }
    }
}
