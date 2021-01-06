#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf.transformations import euler_from_quaternion
from math import atan2, sqrt

from rt_assignment_1.srv import RandomTarget
from rt_assignment_1.srv import RandomTargetRequest
from rt_assignment_1.srv import RandomTargetResponse

current_position_x = 0.0
current_position_y = 0.0
yaw = 0.0


def the_distance_to_target(target):
    """
    Calculates the distance between the robot and the
    target

    Args:
        target (Object): Object containing the x and y
        coodinates of the new target

    Returns:
        (int): returns a tuple of the value of the
        distance to the target and the required yaw to
        face the direction of the target
    """

    dist_x = target.cord_x - current_position_x
    dist_y = target.cord_y - current_position_y
    required_yaw = atan2(dist_y, dist_x)
    distance_to_target = sqrt((dist_x*dist_x) + (dist_y*dist_y))
    return distance_to_target, required_yaw


def call_to_service():
    """
    Sends a service request to random_target with a status
    message

    Returns:
        (Object): A target object containing the x and y
        coordinates
    """
    rospy.wait_for_service('random_target')
    try:
        random_target = rospy.ServiceProxy('random_target', RandomTarget)
        if(current_position_x == 0.0 and current_position_y == 0.0 and yaw == 0.0):
            target = random_target('Waiting for Target')
        else:
            target = random_target('Target Reached')
    except rospy.ServiceException(e):
        # print(f'Service call failed: {e}')
        print('Service call failed: {0}'.format(e))
    return target


def pose_clbk(pose_message):
    """
    The pose callback function takes the position and posture of
    the robot from the argument "pose_message" and set it to
    three global variables containing the x, y and yaw position.

    Args:
        pose_message (Object): an object containing all the values
        of the current position and posture of the robot
    """

    # "global" makes the variable accessible everywhere in the code
    global current_position_x
    global current_position_y
    global yaw

    current_position = pose_message.pose.pose.position
    rotation = pose_message.pose.pose.orientation
    quaternion = [rotation.x, rotation.y, rotation.z, rotation.w]

    current_position_x = current_position.x
    current_position_y = current_position.y

    # Using tuple unpacking to get the roll, pitch and yaw values for the euler tuple
    (roll, pitch, yaw) = euler_from_quaternion(quaternion)


def control():
    """
    The control function sends a request to random_target service,
    accepts a response of the cordinates of the new target position
    and sets the robot to navigate to the target coordinates
    """

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
    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        if (distance_to_target < 0.1):
            velocity.linear.x = 0.0
            if(distance_to_target != 0.0 and current_position_x != 0.0 and current_position_y != 0.0):
                # print(
                #    f'Distance to target: {distance_to_target :.4f}, x: {current_position_x :.4f}, y: {current_position_y :.4f}')
                print('Distance to target: {0:.4f}, x: {1:.4f}, y: {2:.4f}'.format(
                    distance_to_target, current_position_x, current_position_y))
            target = call_to_service()
        distance_to_target, required_yaw = the_distance_to_target(target)
        if (target.cord_x != 0 and target.cord_y != 0):
            if (abs(required_yaw - yaw) > 0.1):
                velocity.linear.x = 0.0
                velocity.angular.z = 0.3
            else:
                velocity.linear.x = 0.5
                velocity.angular.z = 0.0
                distance_to_target, required_yaw = the_distance_to_target(
                    target)
                # print(
                #    f'Distance to target: {distance_to_target :.4f}, x: {current_position_x :.4f}, y: {current_position_y :.4f}')
                print(
                    'Distance to target: {0:.4f}, x: {1:.4f}, y: {2:.4f}'.format(distance_to_target, current_position_x, current_position_y))
            vel_pub.publish(velocity)
        rate.sleep()


if __name__ == '__main__':
    try:
        control()
    except rospy.ROSInterruptException:
        pass
