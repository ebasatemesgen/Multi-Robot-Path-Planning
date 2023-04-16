#!/usr/bin/env python3

import rospy
import actionlib
import numpy as np
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose, Point, Quaternion
from random import randrange
import time
import threading

class Explore:

    def __init__(self, robot_ns):
        self.robot_ns = robot_ns

        # Initialize rate:
        self.rate = rospy.Rate(1)

        # Simple Action Client:
        self.move_base = actionlib.SimpleActionClient('{}/move_base'.format(robot_ns), MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(5.0))
        rospy.logdebug("{}: move_base is ready".format(robot_ns)) 

        self.x = 0
        self.y = 0
        self.completion = 0

        # Initialize subscribers:
        self.map = OccupancyGrid()
        self.sub_map = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        self.count = 0
        time.sleep(8)

    def map_callback(self, data):
        valid = False

        while valid is False:
            map_size = randrange(len(data.data))
            self.map = data.data[map_size]

            edges = self.check_neighbors(data, map_size)
            if self.map != -1 and self.map <= 0.2 and edges is True:
                valid = True

        row = map_size / 384
        col = map_size % 384

        self.x = col * 0.05 - 10
        self.y = row * 0.05 - 10

        if self.completion % 2 == 0:
            self.completion += 1
            self.set_goal()

    def set_goal(self):
        rospy.logdebug(f"{self.robot_ns}: Setting goal")

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.x
        goal.target_pose.pose.position.y = self.y
        goal.target_pose.pose.orientation.w = 1.0
        rospy.logdebug(f"{self.robot_ns}: goal: {goal.target_pose.pose.position.x, goal.target_pose.pose.position.y}")
        self.move_base.send_goal(goal, done_cb=self.goal_status)

    def goal_status(self, status, result):
        self.completion += 1

        if status == 3:
            rospy.loginfo(f"{self.robot_ns}: Goal succeeded")
        if status == 4:
            rospy.loginfo(f"{self.robot_ns}: Goal aborted")
        if status == 5:
            rospy.loginfo(f"{self.robot_ns}: Goal rejected")

    def check_neighbors(self, data, map_size):
        unknowns = 0
        obstacles = 0

        for x in range(-3, 4):
            for y in range(-3, 4):
                row = x * 384 + y
                try:
                    if data.data[map_size + row] == -1:
                        unknowns += 1
                    elif data.data[map_size + row] > 0.65:
                        obstacles += 1
                except IndexError:
                    pass

        if unknowns > 0 and obstacles < 2:
            return True
        else:
            return False

def run_explore(robot_ns):
    explore = Explore(robot_ns)
    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('multi_explore', log_level=rospy.DEBUG)

        tb3_0_thread = threading.Thread(target=run_explore, args=("tb3_0",))
        tb3_1_thread = threading.Thread(target=run_explore, args=("tb3_1",))
        tb3_2_thread = threading.Thread(target=run_explore, args=("tb3_2",))

        tb3_0_thread.start()
        tb3_1_thread.start()
        tb3_2_thread.start()

        tb3_0_thread.join()
        tb3_1_thread.join()
        tb3_2_thread.join()

    except rospy.ROSInterruptException:
        pass
