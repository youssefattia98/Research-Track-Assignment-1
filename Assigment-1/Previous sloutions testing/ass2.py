from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python2 run.py ass2.py

"""

#silver distance
sd=0.0
#silver angle
sa=0.0
#gold ditsnace
gd=0.0
#gold angle
ga=0.0

a_th = 1.0
""" float: Threshold for the control of the linear distance"""

g_th = 0.7

d_th = 0.4
""" float: Threshold for the control of the orientation"""


silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""
def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def gotit():
    """
    function to react to silver token found

    """
    R.grab()
    print("Gotcha!")
    turn(25, 2.35)
    drive(20,1)
    R.release()
    drive(-20,2)
    turn(-25,2.35)


while 1:
    sd, sa = find_silver_token()
    gd, ga = find_golden_token()
    if(gd>g_th): #gold is far and robot is safe
        drive(25,0.5)
        if(sd<d_th):
            gotit()

    elif(gd<=g_th): #gold is near and robot is not safe
        drive(0,1)
        # print('Silver distance is:')
        # print(sd)
        # print('Silver angle is:')
        # print(sa)
        # print('gold distance is:')
        # print(gd)
        # print('gold angle is:')
        # print(ga)
        if(sd<=1.7):#silver is in sight
            if(-a_th<= sa <= a_th): # if the robot is well aligned with the token, we go forward
                print('moving')
                drive(25,0.25)
            if(sd<=d_th):
                gotit()
            elif (sa < -a_th): # if the robot is not well aligned with the token, we move it on the left or on the right
                print("Left a bit...")
                turn(-2, 0.5)
            elif (sa > a_th):
                print("Right a bit...")
                turn(2, 0.5)
        elif(sd>1.5):#silver is far
            print('silver is far')
            print(ga)
            if((ga<90 and ga>0) or (ga<-90 and ga>-180)):
                turn(-20,1.5)
                drive(25,2)
            elif((ga<-180 and ga>90) or (ga<0 and ga>-90)):
                turn(20,1.5)
                drive(25,2.5)