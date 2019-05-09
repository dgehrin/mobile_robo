#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import OccupancyGrid
from roadmap.msg import GridInfo, ObPixels

width = 0
height = 0
data = []

#sub_mapInfo = rospy.Subscriber('/mapinfo', GridInfo, mapInfoCB)#note to self make a calback
#pub_bushMap = rospy.Publisher('/bushfire_map', OccupancyGrid, queue_size=10)

def mapInfoCB(msg):
	print("there is data")
	#print(msg.grid.data)
	global width
  	global height
  	global data
  
  	width = msg.grid.info.width
  	height = msg.grid.info.height
  	data = msg.grid.data
	print("widthb4:", width)
	print("heightb4:", height)
	bushFireAlg()
	
	
def bushFireAlg():
	global data
	global width
	newData = list(data)
	for i,v in enumerate(newData):
		if v == 100:

			if i % width != 0:
				if newData[i-1] != 100:#left
					newData[i-1] = 1
			if i% width != (width -1):
				if newData[i+1] != 100:#right
					newData[i+1] = 1
			if i>(width-1) and i % width != 0:
				if newData[i-width-1] != 100: #Top Left
					newData[i-width-1] = 1
			if i% width != (width -1) and i>(width-1):
				if newData[i-width+1] != 100: #Top RIght
					newData[i-width+1] = 1
			if i>(width-1):
				if newData[i-width] != 100:#up
					newData[i-width] = 1
			if i % width != 0 and i + width < len(newData):
				if newData[i+width-1] != 100:#bot left
					newData[i+width-1] = 1
			if i + width < len(newData):
				if newData[i+width] != 100:#bot 
					newData[i+width] = 1
			if i% width != (width -1) and  i + width < len(newData):
				if newData[i+width+1] != 100:#bot right
					newData[i+width+1] = 1
        
	print(newData)

def main():
	rospy.init_node("roadmap", anonymous = True)
	sub_mapInfo = rospy.Subscriber('/mapInfo', GridInfo, mapInfoCB)#note to self make a calback
	pub_bushMap = rospy.Publisher('/bushfire_map', OccupancyGrid, queue_size=10)
	rospy.sleep(1)
	rospy.spin()
	
main()