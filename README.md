# astrolux-low-fidelity
This is a low fidelity prototype testing my hypothesis that LETth and V/VDSS values can be predicted through MOSFET characteristics. 

# about project
Early satellite failure is becoming an increasingly prominent problem in the space industry. Specifically, satellite failure due to space radiation has been an ongoing problem for decades. 
The root cause of this problem is lack of access to radiation testing methods, in order to assess how electronic components will perform over the course of a satellite mission. 

One of the ways to assess the effectiveness of electronics is by looking at their maximum LET (Linear Energy Transfer) values or maximum operating voltage (V/VDSS or Vmax). This portion of the project aims to see if these values can be predicted through assessing simple MOSFET characteristics. 

All raw data from this project was collected through NASA's GSCE database, and a few values were collected from ESA's Radiation Test Database. 24 values were calculated and manually written, 1000 values were synthetically made from this data using the ctgan library. 
