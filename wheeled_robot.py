#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('turtle_3', anonymous=True)
rate = rospy.Rate(500) # 500hz
pos = 0
angl = 0
def callback(data):
	global pos
	global angl
	pos = data.pose.pose.position
	angl = data.pose.pose.orientation
	print angl
	#print pos

rospy.Subscriber("odom",Odometry,callback)

def drive(time, vel):
	msg = makeMsg(vel,0,0,0,0,0)
	start = rospy.Time.now().to_sec()
	end = start + time
	while rospy.Time.now().to_sec() < end:
		pub.publish(msg)
		rate.sleep()
	msg = makeMsg(0,0,0,0,0,0)
	pub.publish(msg)
    
  
def makeMsg(x,y,z,xa,ya,za):
	msg = Twist()
	msg.linear.x = x
	msg.linear.y = y
	msg.linear.z = z
	msg.angular.x = xa
	msg.angular.y = ya
	msg.angular.z = za
	return msg

def turn(time, vel):
	msg = makeMsg(0,0,0,0,0,vel)
	start = rospy.Time.now().to_sec()
	end = start + time
	while rospy.Time.now().to_sec() < end:
		pub.publish(msg)
		rate.sleep()
	msg = makeMsg(0,0,0,0,0,0)
	pub.publish(msg)

def driveOdom(dist, vel):
	global pos
	#start pos
	spos = pos
	c = 0
	print pos.x
	#if(pos < 1):
		#print("z")
		#while pos == 0:
			#print("first while l")
			#rate.sleep()
	print spos.x + dist
	if(spos.x+dist<pos.x):
		while spos.x + dist < pos.x:
			print str(spos.x + dist) + " < " + str(pos.x)
			print pos.z
			msg = makeMsg(vel,0,0,0,0,0)
			pub.publish(msg)
			rate.sleep()
			c=c+1
			if(c>2000):
				msg = makeMsg(0,0,0,0,0,0)
				pub.publish(msg)
				print ("we dun")
				break
	if(spos.x+dist>pos.x):
		while spos.x + dist > pos.x:
			print str(spos.x + dist) + " > " + str(pos.x)
			print pos.z
			msg = makeMsg(vel,0,0,0,0,0)
			pub.publish(msg)
			rate.sleep()
			c = c+1
			if(c>2000):
				msg = makeMsg(0,0,0,0,0,0)
				pub.publish(msg)
				print ("we dun")
				break

	msg = makeMsg(0,0,0,0,0,0)
	pub.publish(msg)

def turnOdom(rad, vel):
	global angl
	#start angl
	sangl = angl
	c = 0
	goal = sangl.z+rad
	print angl.z
	print sangl.z + rad
	if(goal < angl.z):
		while goal < angl.z:
			print str(goal) + " < " + str(angl.z)
			#print angl.z
			msg = makeMsg(0,0,0,0,0,vel)
			pub.publish(msg)
			rate.sleep()
			c=c+1
			if(1==0):
				msg = makeMsg(0,0,0,0,0,0)
				pub.publish(msg)
				print ("we dun")
				break
	if(goal > angl.z):
		while goal > angl.z:
			print str(goal) + " > " + str(angl.z)
			#print angl.z
			msg = makeMsg(0,0,0,0,0,vel)
			pub.publish(msg)
			rate.sleep()
			c = c+1
			if(1==0):
				msg = makeMsg(0,0,0,0,0,0)
				pub.publish(msg)
				print ("we dun")
				break

	msg = makeMsg(0,0,0,0,0,0)
	pub.publish(msg)
	

if __name__ == '__main__':
	try:
		time.sleep(2)
		#global pos
		turnOdom(.17,.33)
		driveOdom(.1,.1)
		#print pos
		#drive(3,.1)
		#print pos
		#turn(2,.75)
		#turn(2,-.75)
		#print pos
		#drive(3,-.1)
		#print pos
			#print "hi"
      #drive(0,0)
	except rospy.ROSInterruptException:
		pass
