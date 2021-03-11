#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>

signed main(int argc, char * argv[]) {
    char send[175];
    sprintf(send, "mosquitto_pub -t security -m \"xxxxxxxxxx x\" -p 8883 --cafile /usr/security/x509/ca.crt --cert /usr/security/x509/sec.crt --key /etc/mosquitto/certs/sec.key -h <local-IP>", argv[1]);
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
