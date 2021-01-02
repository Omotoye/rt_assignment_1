#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
from random import randint as rand
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt

current_position_x = 0.0
current_position_y = 0.0
yaw = 0.0
rand_x = 0.0
rand_y = 0.0
required_distance = 0.0


def pose_clbk(pose_message):
    global current_position_x
    global current_position_y
    global yaw

    current_position = pose_message.pose.pose.position
    rotation = pose_message.pose.pose.orientation
    quaternion = [rotation.x, rotation.y, rotation.z, rotation.w]

    current_position_x = current_position.x
    current_position_y = current_position.y
    roll, pitch, yaw = euler_from_quaternion(quaternion)


# Initializing the node
rospy.init_node("robot_controller")

# Creating a publisher object
vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

# Creating a subscriber that get the real time location of the robot
pose_sub = rospy.Subscriber("odom", Odometry, pose_clbk, queue_size=10)

# Creating an object to set the frequency
loop_rate = rospy.Rate(4)

# Creating an object for the turtle motion
velocity_v = Twist()


while not rospy.is_shutdown():

    if (required_distance < 0.1):
        velocity_v.linear.x = 0.0
        # Random Location generator
        rand_x = rand(-6.0, 6.0)
        rand_y = rand(-6.0, 6.0)
        print(f'The Destination coordinate is x: {rand_x}, y: {rand_y}')
        
    diff_x = rand_x - current_position_x
    diff_y = rand_y - current_position_y
    required_theta = atan2(diff_y, diff_x)
    required_distance = sqrt((diff_x*diff_x) + (diff_y * diff_y))

    if (abs(required_theta - yaw) > 0.1):
        velocity_v.linear.x = 0.0
        velocity_v.angular.z = 0.3
    else:
        velocity_v.linear.x = 0.5
        velocity_v.angular.z = 0.0
        print(f'x cord: {current_position_x}, y cord: {current_position_y}, Distance to Goal: {required_distance}')

    vel_pub.publish(velocity_v)
    loop_rate.sleep()
