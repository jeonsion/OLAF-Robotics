cmake_minimum_required(VERSION 3.0.2)
project(olaf_navigation)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

roslaunch_add_file_check(launch/amcl.launch)
roslaunch_add_file_check(launch/master.launch)
roslaunch_add_file_check(launch/move_base.launch)


install(
DIRECTORY launch maps params
DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
