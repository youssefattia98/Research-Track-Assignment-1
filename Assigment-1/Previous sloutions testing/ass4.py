from __future__ import print_function

import time
from sr.robot import *

"""
run with:
	$ python2 run.py ass4.py
"""

tokenissilver = 1
turndir=1

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

beforehit = 0.68
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
    turn(20, 3)
    drive(20,2)
    R.release()
    drive(-20,3)
    turn(-20,3)

def silvernear():
    if (sa<-a_th):
        print("Left a bit...")
        turn(-2, 0.5)
    elif(sa>a_th):
        print("Right a bit...")
        turn(+2, 0.5)
    elif (-a_th<= sa <= a_th):
        print("Ah, that'll do.")
        drive(10, 0.5)

drive(20,2)
while 1:
    sd, sa = find_silver_token()
    gd, ga = find_golden_token()


    
    if(gd>beforehit):#i am safe, can move and check for silver
        print('i am safe')
        if(sd<0.7 and tokenissilver==1):
            silvernear()
            if (sd <d_th):
                gotit()
                tokenissilver = 0
                turndir=2
        else:
            drive(20,0.5)

    elif(gd<beforehit):#i am not safe, have to turn
        print('i am not safe i have to turn')
        print('silver distance:')
        print(sd)
        tokenissilver=1
        print('cond1:')
        print(tokenissilver)
        print('cond2')
        print(turndir)
        if(sd<1.9 and (abs(sa))<90 and tokenissilver==1 and (turndir==1 or turndir==2)):
            print('silver is near i can grabe it')
            silvernear()
            if sd<d_th:
                gotit()
                tokenissilver=0
                turndir=0
                print('cond 2 changed to :')
                print(turndir)
        elif(sd>=1.9):
            print('silver is not near i will move according to gold angle')
            if((ga<90 and ga>0) or (ga<-90 and ga>-180)):
                turn(-10, 1)
                drive(10, 1)
            elif((ga<-180 and ga>90) or (ga<0 and ga>-90)):
                turn(+10, 1)
                drive(10, 1)
            turndir=1
