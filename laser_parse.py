#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

pub_scan = rospy.Publisher('/visualization_marker', Marker, queue_size=100)
points = []

#*****************************************************************************************************************
# Use this function to get objects you can send to Rviz!
#
# Parameter 'points' is a list of geometry_msgs/Point objects
# Returns a visualization_msgs/Marker object that can be published to Rviz on topic 'visualization_marker'

# Edit the frame_id assignment below if you're using a TB2 (lines 25 and 28)
#*****************************************************************************************************************
def theCallBack(data):
	global points
	angle_min = data.angle_min
	angle_max = data.angle_max
	angle_inc = data.angle_increment
	range_min = data.range_min
	range_max = data.range_max
	ranges = data.ranges
	points = []
	for n in range(0,len(ranges)-1):
		angle = n*angle_inc+angle_min
		d = ranges[n]
		#print(d)
		x = d*math.cos(angle)
		y = d*math.sin(angle)
		z = 0.0
		point = Point()
		point.x = x
		point.y = y
		point.z = z
		points.append(point)

	#print(points)
	pub_scan.publish(getMarkerWithPoints(points))
	pub_scan.publish(getMarkerWithPoints(points))
	pub_scan.publish(getMarkerWithPoints(points))


def getMarkerWithPoints(points):
    #print 'In plotPoint'

	marker = Marker()

    # TB2
    #marker.header.frame_id = 'camera_depth_frame'

    # TB3
	marker.header.frame_id = 'base_scan'

	marker.header.stamp = rospy.Time(0)
	marker.ns = ''

    # Id of marker will always be 0
	marker.id = 0
	marker.type = 8 # Points
	marker.action = 0 # Add

    # Append the point to the points array
	for p in points:
        # Use p as the point. It should be a PointStamped
		marker.points.append(p)
    
    # Set size 
	marker.scale.x = 0.01
	marker.scale.y = 0.01
	marker.scale.z = 0.01

    # Set color and then append to colors array
	marker.color.r = 1.0
	marker.color.g = 1.0
	marker.color.b = 1.0
	marker.color.a = 1.0
	marker.colors.append(marker.color)

    # Show for 10 seconds. Maybe pass this as a param?
	marker.lifetime = rospy.Duration(10.0)

	return marker


def main():
	global points
	print 'In main'
	rospy.init_node('laser_parse', anonymous=True)


    # Make a subscriber for the /scan topic
    # The /scan topic has sensor_msgs/LaserScan msgs published on it
	sub_scan = rospy.Subscriber('/scan', LaserScan, theCallBack)#note to self make a calback
	
	rospy.spin()

if __name__ == '__main__':
	main()
