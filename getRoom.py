#!/usr/bin/env python3

import rospy
import tf
from nav_msgs.msg import Odometry


def getRoom(x, y):
    if ((x>-7.5 and y >-0.5) and (x< -0.05 and y <7)):
        rospy.loginfo("Room0")
        #center: (-3.5, 3.2)
    elif ((x>-0.05 and y >-2.2) and (x< 5.85 and y <7)):
        rospy.loginfo("Room1")
        #center: (2.9, 2.4)
    elif ((x>7.5 and y >-7.9) and (x< 15 and y <-0.5)):
        rospy.loginfo("Room2")
        #center: (11.25, -5.05)
    elif ((x>-0.05 and y >-7.9) and (x< 7.5 and y <-2.2)):
        rospy.loginfo("Room3")
        #center: (3.725, -5.05)
    elif ((x>-7.5 and y >-7.9) and (x< -0.05 and y <-0.5)):
        rospy.loginfo("Room4")
        #center: (-3.775, -4.2)
    else:
        rospy.loginfo("Room5")
        #exit 1:
        #exit 4:



def getPose(odom):
    currentX = odom.pose.pose.position.x
    currentY = odom.pose.pose.position.y
    currentRoll, currentPitch, currentYaw = tf.transformations.euler_from_quaternion([odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w])
    rospy.loginfo(rospy.get_caller_id() + "  Coordinates: x = " + str(currentX) + "               y = "+ str(currentY))
    rospy.loginfo(rospy.get_caller_id() + " RPY = " + str(currentRoll) +" - " + str(currentPitch) + " - " + str(currentYaw))
    getRoom(currentX, currentY)

 
if __name__ == '__main__':
    try:
        rospy.init_node('maze_solver', anonymous=True)
        rospy.Subscriber("/odom", Odometry, getPose)
        rospy.spin()
    except:
        rospy.loginfo("getRoom currently not working idk")