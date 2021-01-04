#!/usr/bin/python3
from rt_assignment_1.srv import RandomTarget
from rt_assignment_1.srv import RandomTargetRequest
from rt_assignment_1.srv import RandomTargetResponse
from random import randint as rand
import rospy


def handle_random_target(req):
    """
    Takes in a request message and returns a random target
    coordinte, x and y

    Args:
        req (str): The request message sent by the Client

    Returns:
        [Object]: The response sent to the Client 
    """

    print(req)

    # Random Location Generator
    rand_x = rand(-6.0, 6.0)
    rand_y = rand(-6.0, 6.0)
    print(f'The new target cordinate is x: {rand_x}, y: {rand_y}')

    return RandomTargetResponse(rand_x, rand_y)


def random_target_gen():
    """
    Initializes the Service and sends request message to
    the callback function
    """
    rospy.init_node('random_target_gen')
    s = rospy.Service('random_target', RandomTarget, handle_random_target)
    rospy.spin()


if __name__ == '__main__':
    random_target_gen()
