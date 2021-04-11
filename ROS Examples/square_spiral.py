#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist

from turtlesim.msg import Pose

import sys

import math

x = 0.0
y = 0.0
yaw = 0.0

def pose_callback(pose):
    global x, y, yaw
    # rospy.loginfo("Robot X = %f : Y=%f : Z=%f\n",pose.x,pose.y,pose.theta)
    x = pose.x
    y = pose.y 
    yaw = pose.theta


def move(distance, speed):
    global x, y

    distance_traveled = 0
    vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_out = Twist()
    vel_out.linear.y = 0
    vel_out.linear.z = 0
    vel_out.angular.x = 0
    vel_out.angular.y = 0
    vel_out.angular.z = 0

    loop_rate = rospy.Rate(10)
    x0 =  x
    y0 =  y
    rospy.loginfo("%f, %f, %f",distance, x, y)
    while True:
        vel_out.linear.x = speed
        vel_pub.publish(vel_out)
        loop_rate.sleep()

        # rospy.loginfo("Moving {}".format(distance_traveled))
        distance_traveled = math.sqrt((x-x0)**2 + (y-y0)**2)
        if distance_traveled > distance:
            print(distance_traveled)
            break

    vel_out.linear.x=0
    vel_pub.publish(vel_out)
    rospy.loginfo("Reached")


def turn(angle):
    global yaw
    initial = yaw
    target = initial + angle 
    vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_out = Twist()
    if angle > 0:
        while True:
            if target - yaw >= 0.002:
                vel_out.linear.x = 0
                vel_out.linear.y = 0
                vel_out.linear.z = 0
                vel_out.angular.x = 0
                vel_out.angular.y = 0
                vel_out.angular.z = (target-yaw) * 20
                vel_pub.publish(vel_out)
                rospy.loginfo("turning to target %f, currently at %f", target, angle)
            else:
                break
        vel_out.angular.z = 0
        vel_pub.publish(vel_out)
        rospy.loginfo("Finished turn of %f radians", angle)
    else:
        rospy.loginfo("Can't do negative angles yet, sorry!")


def move_turtle(lin_vel,ang_vel):
    global x, y, yaw
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
    
    rate = rospy.Rate(10) # 10hz
 
    vel = Twist()
    while not rospy.is_shutdown():
        
        vel.linear.y = 0
        vel.linear.z = 0

        vel.angular.x = 0
        vel.angular.y = 0

        if x > 9 or x < 2:
            vel.linear.x = lin_vel
            vel.angular.z = ang_vel
        else:
            vel.linear.x = lin_vel
            vel.angular.z = 0

        # rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)

        pub.publish(vel)

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('move_turtle_funcs', anonymous=False)
        rospy.Subscriber('/turtle1/pose',Pose, pose_callback)

        # move_turtle(float(sys.argv[1]),float(sys.argv[2]))
        move(1, 1)
        for i in range(4):
            turn(math.pi/2)
            move(2, 1)
        for i in range(4):
            turn(math.pi / 2)
            move(2.5, 1)
        
    except rospy.ROSInterruptException:
        pass