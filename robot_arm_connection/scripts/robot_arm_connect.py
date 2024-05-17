#! /usr/bin/env python3
import rospy
import actionlib
from robot_arm_connection.msg import FindBookAction, FindBookGoal


from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

##### Motor_define #####
BURGER_MAX_LIN_VEL = 0.3
BURGER_MAX_ANG_VEL = 1.5


##### Robot_arm #####
client = None

def feedback_cb(feedback):
    rospy.loginfo('distance: %f' % feedback.distance)

def book_client():
    global client
    client = actionlib.SimpleActionClient('book_action', FindBookAction)
    client.wait_for_server()

    goal = FindBookGoal(book_name='book3', book_storage="book_storage1")
    

    client.send_goal(goal, feedback_cb=feedback_cb)

    client.wait_for_result()
    rospy.loginfo(client.get_state())
    return client.get_result()



if __name__ == '__main__':



    try:
        rospy.init_node('mobility')
        result = book_client()
        if result:
            rospy.loginfo('is arrived: %s' % result.arrived)
        else:
            rospy.loginfo('Goal was cancelled or failed to execute.')
    except rospy.ROSInterruptException:
        pass

