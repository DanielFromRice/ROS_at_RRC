#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

import math

import sys

x = 5
y = 5
yaw = 0


def pose_callback(pose):
    global x, y, yaw
    # rospy.loginfo("Robot X = %f : Y=%f : Z=%f\n",pose.x,pose.y,pose.theta)
    x = pose.x
    y = pose.y 
    yaw = pose.theta

def move_turtle(lin_vel,ang_vel):
    global x, y, yaw
    angle = 0
    turning = 0
    turn_amt = ang_vel
    rospy.init_node('move_turtle', anonymous=False)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback)

    rate = rospy.Rate(10) # 10hz
 
    vel = Twist()
    while not rospy.is_shutdown():
        
        vel.linear.y = 0
        vel.linear.z = 0

        vel.angular.x = 0
        vel.angular.y = 0

        if turning:
            if yaw < (((math.pi - angle) % (math.pi * 2)) +.1) and yaw > (math.pi - angle)% (math.pi * 2) - .1:
                turning = 0
                vel.linear.x = lin_vel
                vel.angular.z = 0
            else:
                vel.linear.x = 0
                vel.angular.z = turn_amt
        else:
            if x > 9 or x < 2:
                vel.linear.x = 0
                turning = 1
                angle = yaw
                if (yaw > math.pi):
                    turn_amt =  -ang_vel 
                else: 
                    turn_amt =  ang_vel
                vel.angular.z = turn_amt
            else:
                vel.linear.x = lin_vel
                vel.angular.z = 0

        # rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)

        pub.publish(vel)

        rate.sleep()

if __name__ == '__main__':
    try:
        move_turtle(1,2)
    except rospy.ROSInterruptException:
        pass
