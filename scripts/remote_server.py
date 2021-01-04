#!/usr/bin/python3
from rt_assignment_1.srv import RandomTarget
from rt_assignment_1.srv import RandomTargetRequest
from rt_assignment_1.srv import RandomTargetResponse
from random import randint as rand
import rospy

# The callback function
def handle_random_target(req):
    print(req)
    # Random Location Generator
    rand_x = rand(-6.0, 6.0)
    rand_y = rand(-6.0, 6.0)
    print(f'The target cordinate is x: {rand_x}, y: {rand_y}')
    return RandomTargetResponse(rand_x, rand_y)


def random_target_gen():
    rospy.init_node('random_target_gen')
    s = rospy.Service('random_target', RandomTarget, handle_random_target)
    print('Finding new target')
    rospy.spin()


if __name__ == '__main__':
    random_target_gen()
