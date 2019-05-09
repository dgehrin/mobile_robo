#!/usr/bin/env python

import rospy
import math
from nav_msgs.msg import OccupancyGrid
from roadmap.msg import GridInfo, ObPixels

width = 0
height = 0
data = ()

def mapInfoCB(msg):
  global width
  global height
  global data

  width = msg.info.width
  height = msg.info.height
  data = msg.grid.data

  bushFireAlg()


def bushFireAlg():
  global width
  global data

  newData = list(data)
  for i in newData:
    if i == 100: #Ran into error, program saw Tuple but we need a List
      if newData[i-width-1] != 100: #Top Left
        newData[i-width-1] = 1
      if newData[i-width+1] != 100: #Top RIght
        newData[i-width+1] = 1
      if newData[i-width] != 100:#up
        newData[i-width] = 1
      if newData[i-1] != 100:#left
        newData[i-1] = 1
      if newData[i+1] != 100:#right
        newData[i+1] = 1
      if newData[i+width-1] != 100:#bot left
        newData[i+width-1] = 1
      if newData[i+width] != 100:#bot
        newData[i+width] = 1
      if newData[i+width+1] != 100:#bot right
        newData[i+width+1] = 1

    for n in newData:

    print(newData)






def main():
  rospy.init_node('roadmap', anonymous=False)
  sub_mapInfo = rospy.Subscriber('/mapInfo', GridInfo, mapInfoCB) #note to self make a calback
  pub_bushMap = rospy.Publisher('/bushfire_map', OccupancyGrid, queue_size=10)
  rospy.sleep(1)
  #bushFireAlg()
  rospy.spin()


main()
