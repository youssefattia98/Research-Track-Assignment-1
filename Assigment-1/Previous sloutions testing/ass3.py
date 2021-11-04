from __future__ import print_function

import time
from sr.robot import *

"""
run with:
	$ python2 run.py ass3.py
"""

tokenissilver = 1
turndircetion = 1

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

beforehit = 0.75
""" float: Threshold for the minm distance before hitting gold"""

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
    turn(20, 2)
    drive(20,2)
    R.release()
    drive(-20,2)
    turn(-20,2)


drive(20,2)
while 1:
    sd, sa = find_silver_token()
    gd, ga = find_golden_token()


    
    if(gd>beforehit):#i am safe, can move and check for silver
        drive(20, 0.5)
        print('I am safe I can move')
        if(sd<d_th and tokenissilver == 1): #i found silver token
            gotit()
            if (tokenissilver == 1):
                tokenissilver=0
            elif(tokenissilver==0):
                tokenissilver=1
        if(sd<0.9 and tokenissilver == 1):
            if (sa<-a_th):
                print("Left a bit...")
                turn(-2, 0.5)
            elif(sa>a_th):
                print("Right a bit...")
                turn(+2, 0.5)
            elif (-a_th<= sa <= a_th):
                print("Ah, that'll do.")
                drive(10, 0.5)



    elif(gd<beforehit):#i am not safe, have to turn
        #print('I should stop')
        tokenissilver = 1 
        drive(0,1)
        if(ga>=-1):
            print('turn left')
            turn(-20,2)
            drive(20, 1)
        elif(ga<=1):
            print('turn right')
            turn(20,2)
            drive(20, 1)
        else:
            drive(20, 0.5)

        
        # if((ga<90 and ga>0) or (ga<-90 and ga>-180)):
        #     turn(-10, 1)
        #     drive(10, 0.5)
        # elif((ga<-180 and ga>90) or (ga<0 and ga>-90)):
        #     turn(+10, 1)
        #     drive(10, 0.5)

        # print('silver distance:')
        # print(sd)
        # print('silver angle')
        # print(sa)
        # print('gold distance')
        # print(gd)
        # print('gold angle')
        # print(ga)


        #will have to check turn should trun untill a certain range only
