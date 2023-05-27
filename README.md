# MoveSmart

This product is built based on two pressure film sensors RP-S40-ST, and one temperature sensor Si7021. Moreover, two ADCs ADS1115 are added to convert the analogue signal obtained from pressure sensors' circuits to digital signal and allowing which to be transmitted using I2C. 

# 
The RaspberryPi file contains both 
1. the communication between RaspberryPi and database
2. the code for controlling the sensors

The App UI design is for the overall layout of the user interface 

The App Backend code contains all the code for reading and writing of the database and other functions like switching activities, changing of shapes
