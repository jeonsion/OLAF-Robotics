#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32

def reset_ticks():
    rospy.init_node('reset_ticks', anonymous=True)

    left_pub = rospy.Publisher('/left_ticks', Int32, queue_size=10)
    right_pub = rospy.Publisher('/right_ticks', Int32, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    initial_value = Int32()
    initial_value.data = 0  # 초기화 값

    while not rospy.is_shutdown():
        left_pub.publish(initial_value)
        right_pub.publish(initial_value)
        rate.sleep()

if __name__ == '__main__':
    try:
        reset_ticks()
    except rospy.ROSInterruptException:
        pass
