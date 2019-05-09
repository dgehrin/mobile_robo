#!/usr/bin/env python

import rospy
import tf
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
rospy.init_node('drive_with_tf',anonymous = False)
lst = tf.TransformListener()
transit = [0,0]
rotate = 0
pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
'''
twist publish velocity
rospy.shut discheck
update distance from strating
sleep rate
'''



#def drive(trans, dist):
	
#	linear = .5*math.sqrt(math.pow(trans[0],2.0)+math.pow(trans[1],2.0))
#	print(linear)
#	return linear

def drive(distance):
	global transit
	global lst
	t = Twist()
	t.linear.x = 0.2
	t.angular.z = 0
	r = rospy.Rate(30)
	rospy.sleep(1)
	(startTrans, trash) = lst.lookupTransform('/base_footprint','/odom',rospy.Time(0))
	transit = startTrans
	xStartPose = startTrans[0]
	yStartPose = startTrans[1]
	xPose = transit[0]
	yPose = transit[1]
	dRelative = math.sqrt( math.pow( xPose - xStartPose,2) + math.pow( yPose - yStartPose,2) )
	while distance >= dRelative and not rospy.is_shutdown():
		try:
			(transit, rot) = lst.lookupTransform('/base_footprint','/odom',rospy.Time(0))
			xPose = transit[0]
			yPose = transit[1]
			print(rot)
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue
		pub_vel.publish(t)
		dRelative = math.sqrt( math.pow( xPose - xStartPose,2) + math.pow( yPose - yStartPose,2))
		r.sleep()
		#print("things are happening")
	t.linear.x = 0.0
	pub_vel.publish(t)

def turnTo(ang): 
	global rotate
	global lst
	rospy.sleep(1)
	r = rospy.Rate(30)
	t = Twist()
	t.linear.x = 0.0
	t.angular.z = 0.5
	(trans, startRot) = lst.lookupTransform('/base_footprint','/odom',rospy.Time(0))
	startTheta = tf.transformations.euler_from_quaternion(startRot)[2]
	#print(startTheta)
	curTheta = startTheta
	maxTheta = ang + .1
	minTheta = ang - .1
	while curTheta > maxTheta or curTheta < minTheta and not rospy.is_shutdown():
		try:
			(transit, rot) = lst.lookupTransform('/base_footprint','/odom',rospy.Time(0))
			curTheta = tf.transformations.euler_from_quaternion(rot)[2]
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue
		pub_vel.publish(t)
		r.sleep()
	#print(curTheta)
	t.angular.z = 0.0
	pub_vel.publish(t)

def moveToFrame(frame_name):
	global rotate
	global transit
	global lst
	rospy.sleep(1)
	t = Twist()
	r = rospy.Rate(30)
	t.linear.x = 0.2
	t.angular.z = 0.5
	(transit, rot) = lst.lookupTransform('/base_footprint',frame_name,rospy.Time(0))
	xTarPose = transit[0]
	yTarPose = transit[1]
	zTarPose = transit[2]
	#tarTheta = tf.transformations.euler_from_quaternion(rot)[2]
	tarTheta = math.atan2(yTarPose,xTarPose)
	deltaDist = math.sqrt(math.pow(xTarPose,2)+math.pow(yTarPose,2)+math.pow(zTarPose,2))
	turnTo(tarTheta)
	drive(deltaDist)
	#print(deltaDist)

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
	#drive(1)
	#turnTo(1)
	moveToFrame('/odom')

main()
