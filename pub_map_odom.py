#!/usr/bin/env python

import rospy
import tf

from nav_msgs.msg import Odometry


def broadcast():
	br = tf.TransformBroadcaster()
	br.sendTransform((2.5,0.5,0.0), tf.transformations.quaternion_from_euler(0, 0, .785), rospy.Time.now(), "odom", "map")

def main():
    	rospy.init_node('pub_map_odom', anonymous=False)
	r = rospy.Rate(10)

	while not rospy.is_shutdown():
		broadcast()
		r.sleep()

main()



