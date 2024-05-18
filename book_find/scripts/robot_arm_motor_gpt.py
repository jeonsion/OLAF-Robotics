#!/usr/bin/env python3

import rospy
import actionlib
from robot_arm_connection.msg import FindBookAction, FindBookGoal
from geometry_msgs.msg import Twist

##### Robot_arm #####
client = None

def feedback_cb(feedback):
    global pub
    linear_vel = feedback.distance * 0.1  # 이동 거리에 비례하여 속도 조절
    linear_vel = max(min(linear_vel, 0.2), -0.2)  # 최대 0.2, 최소 -0.2로 제한
    twist = Twist()
    twist.linear.x = linear_vel
    pub.publish(twist)

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
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        result = book_client()
        if result:
            rospy.loginfo('is arrived: %s' % result.arrived)
        else:
            rospy.loginfo('Goal was cancelled or failed to execute.')
    except rospy.ROSInterruptException:
        pass
