#! /usr/bin/env python3
import rospy
import actionlib
from robot_arm_connection.msg import FindBookAction, FindBookGoal




from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

##### Motor_define #####
BURGER_MAX_LIN_VEL = 0.3
BURGER_MAX_ANG_VEL = 1.5



#### log 출력 ####
def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output



def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)


def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)




if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('qr_control_motor')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    #/book_action/feedback subscriber
    sub = rospy.Subscriber('/book_action/feedback', FindBookAction, feedback_cb)

    turtlebot3_model = rospy.get_param("model", "burger")

    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0


  try:
    while not rospy.is_shutdown():
    
      
      #print 액션 토픽 출력
