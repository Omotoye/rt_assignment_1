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


def pose_clbk(pose_message):
    global current_position_x
    global current_position_y
    global yaw

    current_position = pose_message.pose.pose.position
    rotation = pose_message.pose.pose.orientation
    quaternion = [rotation.x, rotation.y, rotation.z, rotation.w]

    current_position_x = current_position.x
    current_position_y = current_position.y
    (roll, pitch, yaw) = euler_from_quaternion(quaternion)


def control():
    rand_x = 0.0
    rand_y = 0.0
    distance_to_target = 0.0
    # Initializing the node
    rospy.init_node('robot_controller')
    # Creating a publisher object
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # Creating a subscriber that get the real time location of the robot
    pose_sub = rospy.Subscriber('odom', Odometry, pose_clbk, queue_size=10)
    # Creating an object for the robot motion
    velocity = Twist()
    # Creating an object to set the frequency
    rate = rospy.Rate(4)
    while not rospy.is_shutdown():
        if (distance_to_target < 0.1):
            velocity.linear.x = 0.0
            # Random Location Generator
            rand_x = rand(-6.0, 6.0)
            rand_y = rand(-6.0, 6.0)
            print(f'The target cordinate is x: {rand_x}, y: {rand_y}')

        dist_x = rand_x - current_position_x
        dist_y = rand_y - current_position_y
        required_yaw = atan2(dist_y, dist_x)
        distance_to_target = sqrt((dist_x*dist_x) + (dist_y*dist_y))

        if (abs(required_yaw - yaw) > 0.1):
            velocity.linear.x = 0.0
            velocity.angular.z = 0.3
        else:
            velocity.linear.x = 0.5
            velocity.angular.z = 0.0
            print(
                f'Distance to target: {distance_to_target}, x: {current_position_x}, y: {current_position_y}')
        vel_pub.publish(velocity)
        rate.sleep()


if __name__ == '__main__':
    try:
        control()
    except rospy.ROSInterruptException:
        pass
