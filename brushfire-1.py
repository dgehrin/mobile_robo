#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import OccupancyGrid
from roadmap.msg import GridInfo, ObPixels

width = 0
height = 0
data = []

#sub_mapInfo = rospy.Subscriber('/mapinfo', GridInfo, mapInfoCB)#note to self make a calback
#pub_brushMap = rospy.Publisher('/brushfire_map', OccupancyGrid, queue_size=10)

def mapInfoCB(msg):
	print("there is data")
	#print(msg.grid.data)
	global width
  	global height
  	global data
  
  	width = msg.grid.info.width
  	height = msg.grid.info.height
  	data = msg.grid.data
	print("width:", width)
	print("height:", height)
	brushFireAlg()
	
	
def brushFireAlg():
	global data
	global width
	global height
	pub_brushMap = rospy.Publisher('/brushfire_map', OccupancyGrid, queue_size=100)
	newData = list(data)
	
	
	for i in range(0, width-1):#marks edges as 1's
		if newData[i]!= 100:
			newData[i] = 1#top
			newData[i*100] = 1#left
			newData[(i+1)*100-1] = 1#right
			newData[width*height -i-1] = 1#bottom
			
	val = 1
	curSearch = 100 
	flag = True

	while(flag):
		count = 0
		print("curSearch ", curSearch)
		for i,v in enumerate(newData):
			if v == curSearch:
				if i % width != 0:
					if newData[i-1] == 0:#left
						newData[i-1] = val
						count += 1
				if i% width != (width -1):
					if newData[i+1] == 0:#right
						newData[i+1] = val
						count += 1
				if i>(width-1) and i % width != 0:
					if newData[i-width-1] == 0: #Top Left
						newData[i-width-1] = val
						count += 1
				if i% width != (width -1) and i>(width-1):
					if newData[i-width+1] == 0: #Top RIght
						newData[i-width+1] = val
						count += 1
				if i>(width-1):
					if newData[i-width] == 0:#up
						newData[i-width] = val
						count += 1
				if i % width != 0 and i + width < len(newData):
					if newData[i+width-1] == 0:#bot left
						newData[i+width-1] = val
						count += 1
				if i + width < len(newData):
					if newData[i+width] == 0:#bot 
						newData[i+width] = val
						count += 1
				if i% width != (width -1) and  i + width < len(newData):
					if newData[i+width+1] == 0:#bot right
						newData[i+width+1] = val
						count += 1
		if count == 0:
			flag = False

		if curSearch > 99:
			curSearch = 1
		else:
			curSearch += 1

		val +=1
        
	print(newData)
	banana = OccupancyGrid()
	banana.data = newData
	banana.info.width = width
	banana.info.height = width
	banana.info.resolution = .05
	rospy.sleep(2)
	pub_brushMap.publish(banana)
	pub_brushMap.publish(banana)
	pub_brushMap.publish(banana)

def main():
	rospy.init_node("roadmap", anonymous = True)
	sub_mapInfo = rospy.Subscriber('/mapInfo', GridInfo, mapInfoCB)#note to self make a calback
	
	rospy.sleep(1)
	rospy.spin()
	
main()
