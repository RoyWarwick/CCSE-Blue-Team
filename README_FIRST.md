For the pre-submission testing, Option A (Pre-defined Adressing Option) is desired for the network.

All of the files and documentation that are needed are here in this ("main") branch; this document provides installation instructions.


+---------------+
| Security Unit |
+---------------+

This component uses sensor 2 (the machine with private IPv4 address 192.168.0.4).
The machine must have GPIO pins connected to components in accordance with the diagram stored as "security/security unit circuit diagram.jpg".
The file in this branch stored as "security/security-unit-installation.sh" must be downloaded onto the machine and executed (as the superuser) as its installation script; this script requires no user input or output in order to sucessfully complete.
The script will finish by rebooting the machine and when it starts up again it will be a fully-automated unit.
This can be setup regardless of whether any other machines have been setup; when working, it will wait for the aggregator to be functional.

