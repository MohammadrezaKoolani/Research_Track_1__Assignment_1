# Research Track 1 – First Assignment

This is the first assignment of Research track 1. The aim of this assignment is to find a silver box as shown in Fig.1 in the environment and put them close to a gold box. In the end, all of the silver and golden boxes should be distributed in pairs.

 

![Capture](https://user-images.githubusercontent.com/37951669/218503079-01df3c2c-8ae0-4e93-afeb-f351d83f24fe.PNG)
Figure 1 - The environment of the assignment

Python Robotics Simulator
For doing this project a simple, portable robot simulator developed by student robotics is used. This simulator requires a python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.
To run the simulator use run.py, passing the file names.

```python
$ python run.py assignment.py

```
# Robot API

The API for controlling a simulated robot is designed to be as similar as possible to the SR API.
Motors
The simulated robot has two motors configured for skid steering, connected to a two-output Motor Board. The left motor is connected to output 0 and the right motor to output 1.
The Motor Board API is identical to that of the SR API, except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```


# The Grabber

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the R.grab method:

## success = R.grab()

The R.grab function returns True if a token was successfully picked up, or False otherwise. If the robot is already holding a token, it will throw an AlreadyHoldingSomethingException.
To drop the token, call the R.release method.
Cable-tie flails are not implemented.

### Vision

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The R.see method returns a list of all the markers the robot can see, as Marker objects. The robot can only see markers which it is facing towards.

Each Marker object has the following attributes:

•	info: a MarkerInfo object describing the marker itself. Has the following attributes:
o	code: the numeric code of the marker.
o	marker_type: the type of object the marker is attached to (either MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER or MARKER_ARENA).
o	offset: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
o	size: the size that the marker would be in the real game, for compatibility with the SR API.
•	centre: the location of the marker in polar coordinates, as a PolarCoord object. Has the following attributes:
o	length: the distance from the centre of the robot to the object (in metres).
o	rot_y: rotation about the Y axis in degrees.
•	dist: an alias for centre.length
•	res: the value of the res parameter of R.see, for compatibility with the SR API.
•	rot_y: an alias for centre.rot_y
•	timestamp: the time at which the marker was seen (when R.see was called).

The Explanation of the Code and Functions
All of the functions which are used will be explained in the following:

## drive()

the drive() function was created to allow the robot to move straight, it can go forward, giving to speed parameter a positive value, or it can go backward giving to speed parameter a negative value
•	speed: the linear velocity that we want the robot to assume.
•	seconds: the amount of seconds we want to drive.
•	Returns
o	None.
•	Code

```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```

#### turn()

The turn() functions give the ability of spinning around itself.
•	Arguments
o	speed: the angular velocity that we want the robot to assume.
o	seconds: the amount of seconds we want the robot to turn.
•	Returns
o	None.
•	Code

#### find_silver_token()

This function is used to find silver boxes by using the visionary ability of the robot. The R.see() class returns some list of the markers of silver boxes in which has attributes such as marker_type code, dist, and rot_y.
•	Arguments
o	None.
•	Returns
o	code: identifier of the gold token (-1 if no gold token is detected)
o	dist: distance of the closest silver token (-1 if no silver token is detected)
o	rot_y: angle between the robot and the silver token (-1 if no silver token is detected)
•	Code

```python
def find_silver_token():
    # dist = 100
    silver = list()
    for token in R.see():
       if (token.info.marker_type in (MARKER_TOKEN_SILVER)) and (token.info.code not in grabedSilver):
		tokenInf=[token.info.code, token.dist, token.rot_y]
		silver.append(tokenInf)
		
       print(len(silver),silver)
       if len(silver) == 0:
		print("No silver")
		turn(20,0.5)
		return(find_silver())
       else:
		return(silver)
```


#### find_gold_token()

This function is the same as find_silver_token() function to find the golden boxes.
•	Arguments
o	None.
•	Returns
o	code: identifier of the gold token (-1 if no gold token is detected)
o	dist: distance of the closest silver token (-1 if no silver token is detected)
o	rot_y: angle between the robot and the silver token (-1 if no silver token is detected)
•	Code

```python
def find_gold_token():
    # dist = 100
    gold = list()
    #golds = R.see()
    for token1 in R.see():
       if (token1.info.marker_type in (MARKER_TOKEN_GOLD)) and (token1.info.code not in grbedGold):
		tokenInf1=[token1.info.code, token1.dist, token1.rot_y]
		gold.append(tokenInf1)
		
       print(len(gold),gold)
       if len(gold) ==  0:
            print("There is no gold box")
            turn(20,0.5)
	    return(find_gold_token())
       else:
            return(gold)

```
#### grabSilver()

This function used to grabbing silver boxes using R.grab() class. After grabbing a silver box the function put its information in to a list called grabedSilver.
•	Arguments
o	None.
•	Returns
o	None
•	Code

```python
def grabingSilver(code):

	if R.grab()==True:
		print("Gotcha!")
		grabedSilver.append(code)
		print(grabedSilver)
		
	else:
		print("Noooop!")
```

###### releasingGold()

This function’s responsibility is to releasing silver boxes near the gold ones. When the threshold distance is less than 0.2 it means that robot reaches near the golden boxes with a grabbed silver box and the release it and attaches that gold box to grabedGold list.
•	Arguments
o	None.
•	Returns
o	None
•	Code

```python
def releasingGold(code,dist,rot_y):
              if dist<(d_th + 0.2):
		R.release()
		print("silver and gold are in the same place")
		grabedGold.append(code)
		print(code, grabedGold)
	else:
print("wait....!")
```

###### sortingTokens()

This function sorts the list of tokens. it takes in a list called "list1" as its argument. The purpose of this function is to sort the elements in "list1" based on their second elements (the elements at index 1 of each sublist) in ascending order. Once the list is sorted, the function selects the first element of the sorted list (which will have the lowest value of the second element of each sublist), and assigns its first element to the variable "code", its second element to the variable "dist", and its third element to the variable "rot_y".

•	Arguments
o	list1.
•	Returns
o	Code, dist, rot_y
•	Code

```python
def sortingTokens(list1):
     print(list1)
     list11 = sorted(list1, key = lambda x : x[1])
     code = list11[0][0]
     dist = list11[0][1]
     rot_y = list11[0][2]
     
     return(code, dist, rot_y)
```


