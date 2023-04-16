#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random

class MultiExplore:

    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.cmd_pub = rospy.Publisher('{}/cmd_vel'.format(self.robot_id), Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('{}/scan'.format(self.robot_id), LaserScan, self.scan_callback)
        self.twist = Twist()

    def scan_callback(self, msg):
        self.twist.linear.x = 0.25
        self.twist.angular.z = 0

        min_distance = min(msg.ranges[50:-50])

        if min_distance < 0.5:
            self.twist.linear.x = 0
            self.twist.angular.z = random.uniform(0.5, 1.5)

    def move(self):
        self.cmd_pub.publish(self.twist)

def main():
    rospy.init_node('multi_explore', anonymous=True)

    robot_ids = ['tb3_0', 'tb3_1', 'tb3_2']
    multi_explore = [MultiExplore(robot_id) for robot_id in robot_ids]

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        for explorer in multi_explore:
            explorer.move()
        rate.sleep()

if __name__ == '__main__':
    main()
