#!/usr/bin/python3
import os
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import csv

class SimpleOdomRecorder(object):

    def __init__(self, topic='odom', dir='/home/user/simple_odom_recorder/'):

        rospy.init_node('pose_recorder', anonymous=True)

        ns = rospy.get_namespace()

        self.create_csv(ns, topic, dir)

        self.filewriter.writerow(["Time (s)", "x (m)", "y (m)", "z (m)", "φ (rad)", "θ (rad)","ψ (rad)"])

        self.start_time = rospy.Time.now()

        self.odom_pub = rospy.Subscriber(str(ns) + str(topic), Odometry, self.odom_callback)

    def uniquify(self, path):

        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

    def create_csv(self, ns, topic,dir):
        ns = ns.replace('/', '_')

        if not os.path.exists(dir):
            os.makedirs(dir)

        file_path = os.path.join(dir, (ns[1:] + topic + ".csv") if len(ns) > 1 else (topic + ".csv"))

        file_path = self.uniquify(file_path)

        self.file = open(file_path, 'w')

        self.filewriter = csv.writer(self.file)

    def odom_callback(self, odom_msg):

        timestamp = (rospy.Time.now() - self.start_time).to_sec()

        x = odom_msg.pose.pose.position.x
        y = odom_msg.pose.pose.position.y
        z = odom_msg.pose.pose.position.z

        orientation = odom_msg.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        self.filewriter.writerow([timestamp, x, y, z, roll, pitch, yaw])
        self.file.flush()

if __name__ == '__main__':
    try:
        simple_odom_recorder = SimpleOdomRecorder()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass