#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import OccupancyGrid
from roadmap.msg import GridInfo, ObPixels

sub_voro = 0
pub_voro = 0

width = 0
height = 0
data = []
newData = list(data)

def theCallBack(msg):
	print("there is data")
	global width
  	global height
  	global data
	global newData
	newData = list(data)
  
  	width = msg.info.width
  	height = msg.info.height
  	data = msg.data
	voronoi()

def voronoi():
	global newData
	global width
	newNewData = list(newData)
	global pub_voro
	pub_voro = rospy.Publisher('/voronoi_grid', OccupancyGrid, queue_size=10) 

	for i in range(0,width*width):
		if localMax(i):
			newNewData[i]=0
		else:
			newNewData[i]=127

	print(newNewData)
	banana = OccupancyGrid()
	banana.data = newNewData
	banana.info.width = width
	banana.info.height = width
	banana.info.resolution = .05
	rospy.sleep(2)
	pub_voro.publish(banana)
	pub_voro.publish(banana)
	pub_voro.publish(banana)
	
def localMax(i):
	global width
	global newData
	#i = x + y*width
	curVal = newData[i]
	count = 0

	if curVal == 100:
		return False 
	
	if i % width != 0:
		if newData[i-1] <= curVal or curVal == 100:#left
			count += 1
	if i% width != (width -1):
		if newData[i+1] <= curVal or curVal == 100:#right
			count += 1
	if i>(width-1):
		if newData[i-width] <= curVal or curVal == 100:#up
			count += 1
	if i + width < len(newData):
		if newData[i+width] <= curVal or curVal == 100:#bot 
			count += 1

	if count == 4:
		return True
	else:
		return False
def main():
	rospy.init_node("macandcheese", anonymous = True)
	global sub_voro
	sub_voro = rospy.Subscriber('/brushfire_map', OccupancyGrid, theCallBack)
	
	rospy.sleep(1)
	rospy.spin()
	
main()
	
