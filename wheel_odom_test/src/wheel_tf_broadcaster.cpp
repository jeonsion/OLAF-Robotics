#include <ros/ros.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <nav_msgs/Odometry.h>



// Callback function for odometry messages
void odomCallback(const nav_msgs::Odometry::ConstPtr& msg) {
    static tf2_ros::TransformBroadcaster br;
    geometry_msgs::TransformStamped transformStamped;

    // Set the header
    transformStamped.header.stamp = ros::Time::now();
    transformStamped.header.frame_id = "odom";
    transformStamped.child_frame_id = "base_footprint"; // Adjust frame_id as needed

    // Set the transform translation
    transformStamped.transform.translation.x = msg->pose.pose.position.x;
    transformStamped.transform.translation.y = msg->pose.pose.position.y;
    transformStamped.transform.translation.z = msg->pose.pose.position.z;

    // Set the transform rotation
    transformStamped.transform.rotation.x = msg->pose.pose.orientation.x;
    transformStamped.transform.rotation.y = msg->pose.pose.orientation.y;
    transformStamped.transform.rotation.z = msg->pose.pose.orientation.z;
    transformStamped.transform.rotation.w = msg->pose.pose.orientation.w;

    // Broadcast the transform
    br.sendTransform(transformStamped);
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "wheel_tf_broadcaster");
    ros::NodeHandle nh;

    // Subscribe to the odometry topic
    ros::Subscriber sub = nh.subscribe("odom_data_quat", 10, odomCallback);

    ros::spin();
    return 0;
}
