#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
import tf
import math


class autonav:
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	    # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	    # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

    def ang(self, theta):
        if theta > math.pi:
            return (theta - 2*math.pi)
        elif theta < -math.pi:
            return (theta + 2*math.pi)
        return theta

    def getPose(self, odom):
        self.currentX = odom.pose.pose.position.x
        self.currentY = odom.pose.pose.position.y
        self.currentRoll, self.currentPitch, self.currentYaw = tf.transformations.euler_from_quaternion([odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w])
        #rospy.loginfo(rospy.get_caller_id() + "  Coordinates: x = " + str(self.currentX) + "               y = "+ str(self.currentY))
        #rospy.loginfo(rospy.get_caller_id() + " RPY = " + str(self.currentRoll) +" - " + str(self.currentPitch) + " - " + str(self.currentYaw))

    def move(self,lin,ang):
        #rospy.loginfo("Moving - lin : {} ang : {}".format(lin,ang))
        # Twist is a datatype for velocity
        move_cmd = Twist()
        move_cmd.linear.x = lin
        move_cmd.angular.z = ang
        self.cmd_vel.publish(move_cmd)

    #take the current x, y coordinates, and return the number of room we're currently in
    def getRoom(self, x, y):
        if ((x>-7.5 and y >-0.5) and (x< -0.05 and y <7)):
            rospy.loginfo("Room0")
            return 0
        elif ((x>-0.05 and y >-2.2) and (x< 5.85 and y <7)):
            rospy.loginfo("Room1")
            return 1
        elif ((x>7.5 and y >-7.9) and (x< 15 and y <-0.5)):
            rospy.loginfo("Room2")
            return 2
        elif ((x>-0.05 and y >-7.9) and (x< 7.5 and y <-2.2)):
            rospy.loginfo("Room3")
            return 3
        elif ((x>-7.5 and y >-7.9) and (x< -0.05 and y <-0.5)):
            rospy.loginfo("Room4")
            return 4
        else:
            rospy.loginfo("Room5")
            return 5

    # to go from current (x, y) to target (x2, y2), the robot will first orient itself and then go in a straight line
    def goTo(self, x, y):
        direction = math.atan2(y - self.currentY, x - self.currentX)
        angle_difference = direction - self.currentYaw
        while(abs(self.ang(angle_difference))>0.1):
                    angle_difference = direction - self.currentYaw
                    self.move(0, self.ang(angle_difference))
        while True:
            # Calculate the distance to the target point
            distance = ((x - self.currentX)**2 + (y - self.currentY)**2)**0.5
            
            # If the distance is greater than 0.1, move towards the target point
            if distance > 1.5:
                # Calculate the direction to the target point
                direction = math.atan2(y - self.currentY, x - self.currentX)

                # Calculate the angle difference between the current orientation and the direction to the target point
                angle_difference = direction - self.currentYaw
                angle_difference = self.ang(angle_difference)

                self.move(0.5, self.ang(angle_difference))
                
            else:
                rospy.loginfo("Here.")
                self.move(0, 0)
                break

    def goToRoom(self, n):
        currentRoom = self.getRoom(self.currentX, self.currentY)
        if (currentRoom==0):
            self.goTo(-2, 3.657)                                #home position in Room 0
            rospy.sleep(2)    
            if (n == 4):
                rospy.loginfo("Currently in Room 0, going to room 4")
                self.goTo(-0.9218, -1.5061)                     #door between 0 and 4
                rospy.sleep(2)
                self.goTo(-3.13774, -4.65811)                   #home position in Room 4
                rospy.loginfo("Currently in Room 4!")
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")
        elif (currentRoom)==1:
            self.goTo(1.5, 0.5)                                 #home position in Room 1
            rospy.sleep(2)
            if (n == 3):
                rospy.loginfo("Currently in Room 1, going to room 3")
                self.goTo(1, -2.8)                            #door between 1 and 3
                rospy.sleep(2)
                self.goTo(3.23, -5.23)                          #home position in Room 3
            elif(n == 5):
                rospy.loginfo("Currently in Room 1, going to room 5")
                self.goTo(5.7,0.3)                              #door between 1 and 5
                rospy.sleep(2)
                self.goTo(8.7,4)                                #home position in room 5 (1 exit)
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")
        elif (currentRoom==2):
            self.goTo(12, -5.8)                                 #home position in Room 2
            rospy.sleep(2)
            if (n ==3):
                rospy.loginfo("Currently in Room 2, going to room 3")
                self.goTo(7.4, -6.8)                            #door between 2 and 3
                rospy.sleep(2)
                self.goTo(3.23, -5.23)                          #home position in room 3
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")
        elif (currentRoom==3):
            self.goTo(3.23, -5.23)                              #home position in Room 3
            rospy.sleep(2)
            if (n==1):
                rospy.loginfo("Currently in Room 3, going to room 1")    
                self.goTo(1, -2.8)                            #door between 1 and 3
                rospy.sleep(2)
                self.goTo(1.5, 0.5)                             #home position in room 1
            elif(n==2):
                rospy.loginfo("Currently in Room 3, going to room 2")
                self.goTo(7.4, -6.8)                            #door between 3 and 2
                rospy.sleep(2)
                self.goTo(12, -5.8)                             #home position in room 2
            elif(n==4):
                rospy.loginfo("Currently in Room 3, going to room 4")
                self.goTo(-0.5, -7.4)                           #door between 3 and 4
                rospy.sleep(2)
                self.goTo(-3.13774, -4.65811)                   #home position in room 4
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")
        elif (currentRoom==4):
            self.goTo(-3.13774, -4.65811)                       #home position in Room 4
            rospy.sleep(2)
            if (n==0):
                rospy.loginfo("Currently in Room 4, going to room 0")
                self.goTo(-0.9218, -1.5061)                     #door between 4 and 0
                rospy.sleep(2)
                self.goTo(-2, 3.657)                            #home position in room 0
            elif (n==3):
                rospy.loginfo("Currently in Room 4, going to room 3")
                self.goTo(-0.5, -7.8)                            #door between 4 and 3
                rospy.sleep(2)
                self.goTo(3.23, -5.23)                           #home position in room 3
            elif (n==5):
                rospy.loginfo("Currently in Room 4, going to room 5 (the thin one)")
                self.goTo(-7.2, -7.2)                            #door between 4 and 5
                rospy.sleep(2)
                self.goTo(-5.66, -9.594)                         #home position in room 5 (4 exit)
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")
        elif (currentRoom==5):
            if (n==1):
                rospy.loginfo("Currently in Room 5, going to room 1")
                self.goTo(8.7,4)                                #home position in Room 5 (closer to 1)
                rospy.sleep(2)
                self.goTo(5.7,0.3)                              #door between 1 and 5
                rospy.sleep(2)
                self.goTo(1.5, 0.5)                             #home position in room 1
            elif (n==4):
                rospy.loginfo("Currently in Room 5, going to room 4")
                self.goTo(-5.66, -9.594)                        #home position in Room 5 (closer to 4)
                rospy.sleep(2)
                self.goTo(-7.2, -7.2)                           #door between 4 and 5
                rospy.sleep(2)
                self.goTo(-3.13774, -4.65811)                   #home position in room 4
            else:
                rospy.loginfo("The room you entered isn't adjacent to the current room.")

    #this function uses the q table to go from whichever point it is in to Room 5 in the shortest path.
    def demo(self):
        q_table = [[0,0,0,0,400,0], [0,0,0,320,0,500], [0,0,0,320,0,0], [0,400,256,0,400,0], [320,0,0,320,0,500], [0,400,0,0,400,500]]
        
        currentRoom = self.getRoom(self.currentX, self.currentY)
        while (currentRoom!=5):
            targetRoom = q_table[currentRoom].index(max(q_table[currentRoom]))
            self.goToRoom(targetRoom)
            currentRoom = self.getRoom(self.currentX, self.currentY)

    def __init__(self, targetX = 0, targetY = 0):
        rospy.init_node('autonav', anonymous=False)

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)

        rospy.Subscriber("/odom", Odometry, self.getPose)
        
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
     
	    #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10)
        rospy.sleep(1)
        
        while (True):
            rospy.loginfo("    ")
            rospy.loginfo("To go to an adjacent room, enter its number.")
            rospy.loginfo("Enter 'd' to find the shortest path till room 5")
            rospy.loginfo("Enter 'g' to go to the specified xy coordinates")
            rospy.loginfo("Enter 'c' to exit.")
            usr = input("Enter Here: ")
            if usr == "0":
                self.goToRoom(0)
            elif usr == "1":
                self.goToRoom(1)
            elif usr == "2":
                self.goToRoom(2)
            elif usr == "3":
                self.goToRoom(3)
            elif usr == "4":
                self.goToRoom(4)
            elif usr == "5":
                self.goToRoom(5)
            elif usr == "g" or usr == "G":
                self.goTo(targetX, targetY)
            elif usr == "d" or usr == "D":
                self.demo()
            elif usr == "c" or usr == "C":
                break
            else:
                rospy.loginfo("Sorry, I didn't understand that. Please try again.")
        rospy.spin()


 
if __name__ == '__main__':
    try:
        autonav()
    except:
        rospy.loginfo("autonav node not working.")