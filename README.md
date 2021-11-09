# Research-Track-Assigment-1 description:
Assignment 1 for Research Track course, the project consist of a simulation in which a robot should complete a track without colliding in gold walls and removes any silver obstacle that face it.
This repo consits of the following points:  
 1)How to Setup the Simulator.  
 2)How to use the Simulator.  
 3)Algotirthm used to solve the probelm and flowchart.  
 4)Final output.  
 5)Possible imporovemnts.  

1)How to Setup the Simulator.  
================================

Firstly,this is a simple portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

```bash
$ sudo apt-get install python-dev python-pip python-pygame python-yaml
$ sudo pip install pypybox2d
```

Once the dependencies are installed, get inside the directory on the shell. To run the game, run the command:

```bash
$ python2 run.py Solution.py
```
2)How to use the Simulator.  
================================
Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

3)Algotirthm used to solve the probelm and flowchart. 
================================
There are plenty of Algorithms that can be used to solve this assigment which i have tried more one algorithms, all previous trials can be found in the folder Solutions. However, the most efficient algorithm by far is used in the solution, in whitch the robot turn according to his ditance with the right wall and left wall same as autonomous cars algorithm to follow a lane. This will be explained more further down bellow, in the meantime thwe most challings part of the script is how the robot decides which direction it should turn.  

Flowchart
---------
![immagine](https://github.com/youssefattia98/Research-Track-Assigment-1/blob/main/RTassigment.png)  

The above Flowchart describes in details the working algorithm of the solution. However, some functions needs to be read as script for further understanding how the robot understands its environment and behaves according to this understanding. 

Functions
---------
### how_to_turn() ###
The `how_to_turn()` function is used to see all the tokens around the robot and filter the gold ones, and see the nearest golden token on the robots left and right. by comparing these distances the robot can decide what direction should turn.  
- Arguments 
  - None.
- Returns
  - Returns direction of the turn either -1 or 1.
- Code
```python
    leastdistr=100
    leastdistl=100

    #should look all the left and right only the gold ones.
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
    #The first two condtions are for error handling.
    if(leastdistr==100):
        print('i should rotate anticlockwise')
        return -1
    elif(leastdistl==100):
        print('i should rotate clockwise')
        return 1
    elif(leastdistr>leastdistl):
        print('i should rotate clockwise')
        return 1
    elif(leastdistr<leastdistl):
        print('i should rotate anticlockwise')
        return -1
```
### silvernear() ###
The `silvernear()` function is used to head the robot towards the silver token, grab it and drop it behind the robot.

- Arguments 
  - None.
- Returns
  - None.
- Code
```python
    """
    function to react to silver token found

    """
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
        R.grab()
        print("Gotcha!")
        turn(20, 3)
        R.release()
        turn(-20,3)
```
### find_silver_token() ###
The `silvernear()` function is used to find the closest silver token.
- Arguments 
  - None.
- Returns
  - dist (float): distance of the closest silver token (-1 if no silver token is detected)
	 -rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
- Code
```python
    dist=100
    for token in R.see():
        if ((token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_SILVER)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return None
    else:
        return dist, rot_y
```
### find_golden_token() ###
The `silvernear()` function is used to find the closest golden token.
- Arguments 
  - None.
- Returns
  - dist (float): distance of the closest silver token (-1 if no silver token is detected)
	 -rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
- Code
```python
    dist=100
    for token in R.see():
        if ((token.dist < dist) and (token.info.marker_type is MARKER_TOKEN_GOLD)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y
```
### drive() ###
The `drive()` function is used for setting a linear velocity.
- Arguments 
  - speed (int): the speed of the wheels.
  - seconds (int): the time interval.
- Returns
  - None.
- Code
```python
     R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
### Turn() ###
The `Turn()` function is used for setting a angular velocity.
- Arguments 
  - speed (int): the speed of the wheels.
  - seconds (int): the time interval.
- Returns
  - None.
- Code
```python
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
4)Final Output. 
================================
The speed up video below shows the robot behaving in the environment doing its intended task, this simulation can run for ever in which the robot will stay in this loop. Furthermore, this assigment enhanced my skills in using linux, docker, github, python and object oriented progaramming and i am very happy with the output i have reached.

5)Possible imporovemnts .  
================================
I suggest multiple imporvments which are as follow:  
	1) Apply the function `how to turn()` on the robots motion aroudn the track, this can keep it more safe and avoid collisions as for autonomous cars.  
	2) Apply a Proportional, Integral, Derivative (PID) controller on the robot so it can make the track in the least possible time and changing its drving 	   and turn speeds according to the feedback of the readings. 
![immagine](https://blog.west-cs.com/hs-fs/hub/331798/file-489926128-gif/Blog_Pictures/What_is_PID_Control.gif?t=1528717719517)  
