#!/usr/bin/env python3

import rospy
import actionlib
from robot_arm_connection.msg import FindBookAction, FindBookGoal
from geometry_msgs.msg import Twist

##### Robot_arm #####
client = None

Minimum_distance = -79.0
Maximum_distance = -71.0


def feedback_cb(feedback):
    global pub

    twist = Twist()

    if feedback.distance >= Minimum_distance and feedback.distance <= Maximum_distance:
        twist.linear.x = 0
    elif feedback.distance < Minimum_distance:
        linear_vel = feedback.distance * 0.01
        linear_vel = max(min(linear_vel, 0.02), -0.02)
        twist.linear.x = linear_vel
    elif feedback.distance > Maximum_distance:
        if feedback.distance > 0:
            linear_vel = feedback.distance * 0.01
        else:
            linear_vel = feedback.distance * -0.01

        linear_vel = max(min(linear_vel, 0.03), -0.03)
        twist.linear.x = linear_vel
        
    pub.publish(twist)

def book_client():
    global client
    client = actionlib.SimpleActionClient('book_action', FindBookAction)
    client.wait_for_server()

    goal = FindBookGoal(book_name='book2', book_storage="book_storage1")
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
            twist = Twist()
            twist.linear.x = 0
            pub.publish(twist)
            rospy.loginfo('Motor Stop')

        else:
            rospy.loginfo('Goal was cancelled or failed to execute.')
    except rospy.ROSInterruptException:
        pass
