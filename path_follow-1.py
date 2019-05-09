#!/usr/bin/env python

import math
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import numpy
import rospy
import tf

pose = Pose()
path = Path()
pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)

def callbackPath(data):
	global path
	path = data.poses
	for p in path:
		moveTo(p.pose.position.x, p.pose.position.y)

def callbackOdom(data):
	global pose
	pose = data.pose.pose
	#print(pose)

def driveFor(d, speed):
	global pose
    # The position before we start moving
	p_start = pose.position
    # Create a Twist msg to send
	t = Twist()
	t.linear.x = speed
	t.angular.z = 0
	# Create a rate to send msgs
	r = rospy.Rate(30)
	dRelative = 0
	while dRelative < d and not rospy.is_shutdown():

	    	# Get distance between current position and starting position
		dRelative = math.sqrt( math.pow( pose.position.x - p_start.x,2) + 
			math.pow( pose.position.y - p_start.y,2) )
		# Publish and sleep
		pub_vel.publish(t)
		r.sleep()
		print(dRelative)

def turnTo(rad, speed):
	global pose
    
	if rad >= math.pi:
		rad = math.pi - 0.02
	elif rad <= -math.pi:
		rad = -math.pi + 0.02
    
	currentTheta = tf.transformations.euler_from_quaternion( [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2]
    
	thetaRelative = 0
	t = Twist()
	t.linear.x = 0
	t.angular.z = speed
	r = rospy.Rate(30)
	while currentTheta < rad and not rospy.is_shutdown():
		currentTheta = tf.transformations.euler_from_quaternion([pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2]
		pub_vel.publish(t)
        	r.sleep()
		print(currentTheta)

def moveTo(xPos, yPos):
	global pose
	driveSpd = .2
	turnSpd = .2
	startX = pose.position.x
	startY = pose.position.y
	print(startX)
	print(startY)
	driveDist = findDist(startX, startY, xPos, yPos)
	turnRad = findTheta(startX, startY, xPos, yPos)
	turnTo(turnRad, turnSpd)
	driveFor(driveDist, driveSpd)
	

def findTheta(aX, aY, bX, bY): #a and b are points
	xDetermine = bX - aX
	yDetermine = bY - aY
	return math.atan2(yDetermine, xDetermine)

def findDist(aX, aY, bX, bY):
	x1 = aX - bX 
	y1 = aY - bY
	dist = math.sqrt(x1**2 + y1**2)
	return dist

def findDistanceBetweenAngles(a, b):
	difference = b - a
	print difference
	if difference > math.pi:
		difference = math.fmod(difference, math.pi)
		result = difference - math.pi
	elif(difference < -math.pi):
		result = difference + (2*math.pi)
	else:
		result = difference
	return result

def main():
	global pos
	rospy.init_node('turtle_path', anonymous = True)
	rospy.Subscriber("/path", Path, callbackPath)
	rospy.Subscriber("/odom", Odometry, callbackOdom)
	rospy.sleep(1)
	rospy.spin()
	#driveFor(1,.5)
	#turnTo(math.pi,.3)
	#driveFor(.5,.5)
	#turnTo(.75,.3)
	
	#moveTo()

main()
