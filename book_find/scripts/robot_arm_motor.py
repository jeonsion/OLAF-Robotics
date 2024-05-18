#!/usr/bin/env python3
import rospy
import actionlib
from robot_arm_connection.msg import FindBookAction, FindBookGoal, FindBookFeedback
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, select, os

if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

##### Motor_define #####
BURGER_MAX_LIN_VEL = 0.2
BURGER_MAX_ANG_VEL = 1.5

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26, Gaemi : ~ 0.02)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82, Gaemi : ~ 0.05)

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

#### log 출력 ####
def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel, target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min(input, output + slop)
    elif input < output:
        output = max(input, output - slop)
    else:
        output = input
    return output

def constrain(input, low, high):
    if input < low:
        input = low
    elif input > high:
        input = high
    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
        vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
        vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    return vel

#### Robot_ARM ####
def feedback_cb(feedback):
    global target_linear_vel, target_angular_vel, status, control_linear_vel, control_angular_vel


    if feedback.distance < -1:
        target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
        print(vels(target_linear_vel,target_angular_vel))

    elif feedback.distance > 1:
        target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
        print(vels(target_linear_vel,target_angular_vel))

    else:
        target_linear_vel = 0


    twist = Twist()
    control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
    twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

    control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

    pub.publish(twist)



def book_client():
    client = actionlib.SimpleActionClient('book_action', FindBookAction)
    client.wait_for_server()

    goal = FindBookGoal(book_name='book3', book_storage='book_storage1')
    client.send_goal(goal, feedback_cb=feedback_cb)

    client.wait_for_result()
    rospy.loginfo(client.get_state())
    return client.get_result()

if __name__ == '__main__':
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    turtlebot3_model = rospy.get_param('model', 'burger')

    status = 0
    target_linear_vel = 0.0
    target_angular_vel = 0.0
    control_linear_vel = 0.0
    control_angular_vel = 0.0

    try:
        rospy.init_node('mobility')
        result = book_client()
        if result:
            rospy.loginfo('is arrived: %s' % result.arrived)
        else:
            rospy.loginfo('Goal was cancelled or failed to execute.')
    except rospy.ROSInterruptException:
        pass
