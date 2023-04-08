import random
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Turtlebot:
    def __init__(self, name):
        self.name = name
        self.move_random = Twist()
        self.pub = rospy.Publisher(f"/{name}/cmd_vel", Twist, queue_size=10)
        self.sub = rospy.Subscriber(f"/{name}/scan", LaserScan, self.callback)

    def callback(self, laser):
        threshold = 1
        random_velocity_linear_x = random.randint(-5, 5)
        random_velocity_angualr_z = random.randint(-5, 5)

        if laser.ranges[0] > threshold and laser.ranges[15] > threshold and laser.ranges[345] > threshold:
            if random_velocity_linear_x > 0:
                self.move_random.linear.x = random_velocity_linear_x
                self.move_random.angular.z = random_velocity_angualr_z
            else:
                self.move_random.linear.x = 0
                self.move_random.angular.z = random_velocity_angualr_z
        else:
            if random_velocity_linear_x > 0:
                self.move_random.linear.x = 0.0
                self.move_random.angular.z = random_velocity_angualr_z
            else:
                self.move_random.linear.x = random_velocity_linear_x
                self.move_random.angular.z = 0

            if laser.ranges[0] > threshold and laser.ranges[15] > threshold and laser.ranges[345] > threshold:
                self.move_random.linear.x = random_velocity_linear_x
                self.move_random.angular.z = 0.0

        self.pub.publish(self.move_random)



def stop_turtlebots(turtlebots):
    stop_twist = Twist()
    for tb in turtlebots:
        tb.pub.publish(stop_twist)
    print("shutdown time!")

if __name__ == "__main__":
    rospy.init_node('trying_to_avoidance_obestacle')
    rate = rospy.Rate(10)

    turtlebot_names = ['tb3_0', 'tb3_1', 'tb3_2']
    turtlebots = [Turtlebot(name) for name in turtlebot_names]

    rospy.on_shutdown(lambda: stop_turtlebots(turtlebots))
    
    try:
        rospy.spin()
    except:
        print("error")
