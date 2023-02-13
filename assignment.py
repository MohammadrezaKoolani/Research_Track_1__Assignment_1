from __future__ import print_function

import time
from sr.robot import *

R = Robot() # instance of the class robot

a_th = 2.0 # float, Threshold for control of the orientation

d_th = 0.4 # float, Threshold for control of the distance

grabedSilver = list()
detectedGold = list()

#Silver = True

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
    Function for finding Silver boxes
    For the visionary of robot, The R.see class returns list of the markers and from
    the marker object attributes such as marker_type (gold or silver), dist(the distance
    from the centre of the robot to the object  in metres.) and, rot_y(rotation about the Y axis in degrees.) are used.
    
    """

    # dist = 100
    silver = list()
    global grabedSilver
    for token in R.see():
       if (token.info.marker_type in (MARKER_TOKEN_SILVER)) and (token.info.code not in grabedSilver):
		tokenInf=[token.info.code, token.dist, token.rot_y]
		silver.append(tokenInf)
		
    print(len(silver),silver)
    if len(silver) == 0:
        print("No silver")
        turn(20,0.5)
        return(find_silver_token())
    else:
	return(silver)
        
def find_gold_token():
    """
    Function for finding Gold boxes
    For the visionary of robot, The R.see class returns list of the markers and from
    the marker object attributes such as marker_type (gold or silver), dist(the distance
    from the centre of the robot to the object  in metres.) and, rot_y(rotation about the Y axis in degrees.) are used.
    """

    # dist = 100
    golds = list()
    global detectedGold
    golds1 = R.see()
    for token1 in golds1:
       #print(detectedGold)
       if (token1.info.marker_type in (MARKER_TOKEN_GOLD)) and (token1.info.code not in detectedGold):
		tokenInf1=[token1.info.code, token1.dist, token1.rot_y]
		print("*****************************************************************")
		golds.append(tokenInf1)
		
    print(len(golds),golds)
    if len(golds) ==  0:
        print("There is no gold box")
        turn(20,0.5)
	return(find_gold_token())
    else:
        return(golds)



def grabingSilver(code):
	""" The Function uses R.grab() to pick up the Silver boxes. It returns true 
	if pick the box successfully and returns fals if already holding a box 
	
	"""
	if R.grab()==True:
		print("Gotcha!")
		grabedSilver.append(code)
		print(grabedSilver)
		
	else:
		print("Noooop!")
		
def releasingGold(code,dist,rot_y):
	"""
	Function drops the token when R.release is called
	"""
	if dist<(d_th + 0.2):
		R.release()
		print("silver and gold are in the same place")
		detectedGold.append(code)
		print(code, detectedGold)
	else:
		print("wait....!")
		
def sortingTokens(list_token):
	"""
	Function to sort the tokens with respect to the closest one whithout other tokens in between
	"""
	#sort the list
	print(list_token)
	lt= sorted(list_token, key=lambda x: x[1])
    	#check there are no tokens on my path
    	code=lt[0][0]
        dist=lt[0][1]
        rot_y=lt[0][2]
        return(code, dist, rot_y)

###############################################################################################
####################                                                       ####################
####################                          MAIN                         ####################
####################                                                       #################### 
###############################################################################################
while len(grabedSilver) <= 6:
      print("""
     let's start...
      searching for a silver box!!
      """)
      silver = find_silver_token()                              # First step is finding silvers
      print("choosing the nearest silver box", silver)
      (code, dist, rot_y) = sortingTokens(silver)               # sorting the information of the silvers
      while code not in grabedSilver:                           # when robot reaches closest silver box        
           print("looking for a silver box", code)
           silver = find_silver_token()
           (code, dist, rot_y) = sortingTokens(silver)
           if dist < d_th:                                       # This condition is use to reach the closest Token and if the 
		if -a_th <= rot_y <= a_th:                        # and if the distance of token is less than the threshold 
			print("Ah, That'll do.")                   
			drive(10, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
	   else:                                                 # if the token has too much distance from the robot 
   		if -a_th <= rot_y <= a_th:
			print("Here we are")
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
		print("let's get closer...")
		drive(20,1) 
           grabingSilver(code)                                  # After reaching to the silver boxes, they
                                                                # will be grasbed by the robot
      print("""                                                 
      I have to search for a gold box.
      let's go...
      """)
      gold1 = find_gold_token()                                 # finding Golden token and the same process will be done 
      print("choosing the nearest gold box", gold1)             # as silver boxes
      (code1, dist1, rot_y1) = sortingTokens(gold1)
      while code1 not in detectedGold:
           print("looking for a gold box", code1)
           gold1 = find_gold_token()
           (code1, dist1, rot_y1) = sortingTokens(gold1)
	   if dist < d_th:
		if -a_th <= rot_y <= a_th:
			print("Ah, That'll do.")
			drive(10, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
	   else:
   		if -a_th <= rot_y <= a_th:
			print("Here we are")
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
		print("let's get closer...")
		drive(20,1)
           releasingGold(code1, dist1, rot_y1)                  # When the robot reaches to the gold box it will release silver
           
           

 

      

 

    
