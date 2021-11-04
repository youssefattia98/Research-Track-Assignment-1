from __future__ import print_function

import time
from sr.robot import *

"""

	When done, run with:
	$ python2 run.py ass6.py

"""
a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

beforehit = 1
""" float: Threshold for the minm distance before hitting gold"""

R = Robot()
""" instance of the class Robot"""


beforehit = 0.75
""" float: Threshold for the minm distance before hitting gold"""

markers = R.see()


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

def how_to_turn():

    leastdistr=100
    leastdistl=100

    #should look all the left and right only the fron ones.
    for m in R.see():
        if (m.info.marker_type in (MARKER_TOKEN_GOLD)):
            if(-105<m.rot_y<-75):
                #print(" On my left:{0} metres away and {1} degress".format(m.dist, m.rot_y))
                if(m.dist<leastdistl):
                    print("the left token distance is: {0}",m.dist)
                    leastdistl=m.dist



            if(105>m.rot_y>75):
                #print(" On my right:{0} metres away and {1} degress".format(m.dist, m.rot_y))
                if(m.dist<leastdistr):
                    print("the right token distance is: {0}",m.dist)
                    leastdistr=m.dist

    if(leastdistr==100):
        print('i should go anticlockwise')
        return -1
    elif(leastdistl==100):
        print('i should go clockwise')
        return 1
    elif(leastdistr>leastdistl):
        print('i should go clockwise')
        return 1
    elif(leastdistr<leastdistl):
        print('i should go anticlockwise')
        return -1

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if ((token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_SILVER)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return None
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
        if ((token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_GOLD)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

def silvernear():
    if (sa<-a_th):
        print("Left a bit...")
        turn(-2, 0.5)
    elif(sa>a_th):
        print("Right a bit...")
        turn(+2, 0.5)
    elif (-a_th<= sa <= a_th):
        print("Ah, that'll do.")
        drive(25, 0.5)
    if(sd<d_th):
        gotit()

def gotit():
    """
    function to react to silver token found

    """
    R.grab()
    print("Gotcha!")
    turn(20, 3)
    R.release()
    turn(-20,3)




drive(50,2)
while 1:
    sd, sa = find_silver_token()
    gd, ga = find_golden_token()

    if(gd>beforehit):
        print('gold is far')
        if(sd<1 and (-60 < sa < 60)):
            print('silver is in sight')
            silvernear()
        else:
            print('silver not in sight')
            drive(25,0.5)



    elif(gd<=beforehit and (-90<= ga <=90)):
        print('gold is near stoping')

        if(sd<2 and (-60 < sa < 60)):
            print('silver is in sight')
            silvernear()

        else:
            print('silver not in sight')
            dir= how_to_turn()
            while(abs(ga)<80):
                turn(dir*10,0.5)
                gd, ga = find_golden_token()
                print(ga)
            drive(25,0.5)



    else:
        print('last conditon')
        drive(50,0.25)