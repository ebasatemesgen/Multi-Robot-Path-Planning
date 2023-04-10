#!/usr/bin/env python3

import rospy
from gazebo_ros import gazebo_interface
import rospkg

def main():
    rospy.init_node("spawn_multi_turtlebot3")
    num_robots = rospy.get_param("~num_robots", 2)
    model = rospy.get_param("~model", "burger")
    x_pos = rospy.get_param("~x_pos", 0.0)
    y_pos = rospy.get_param("~y_pos", 0.0)
    spacing = rospy.get_param("~spacing", 2.0)
    slam_methods = rospy.get_param("~slam_methods", "gmapping")

    rospack = rospkg.RosPack()
    model_path = rospack.get_path("turtlebot3_description") + "/urdf/" + model + ".gazebo.xacro"

    for i in range(num_robots):
        robot_namespace = "tb3_" + str(i)
        robot_x = x_pos + i * spacing
        robot_y = y_pos

        gazebo_interface.spawn_sdf_model_client(
            model_name=robot_namespace,
            model_xml=gazebo_interface.xacro_to_urdf(model_path),
            robot_namespace=robot_namespace,
            initial_pose=(robot_x, robot_y, 0, 0, 0, 0),
            reference_frame="world"
        )

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

