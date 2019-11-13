#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32


class NodeExample():

    # Initialization happens when the object is created:
    def __init__(self):

        # Set up a publisher called "publish", for an int
        self.pub = rospy.Publisher(
                "publish",
                Int32,
                queue_size=1)

        # Set up a subscriber called "subscribe" as a String
        self.sub = rospy.Subscriber(
                "subscribe",
                String,
                self.callback)

    def example_function(self):

        val = 0
        rate = rospy.Rate(1) # update rate of 1hz

        while not rospy.is_shutdown():

            rospy.loginfo("publishing value: " + str(val))
            # publish the value val to the topic
            self.pub.publish(val)

            val = val + 1
            # sleep the amount of time needed to achieve the 1hz rate set above
            rate.sleep()


    def callback(self, data):

        # Print the string stored in the ROS String msg:
        rospy.loginfo("I heard: " + data.data)



if __name__ == '__main__':
    # initialization of the ros node
    rospy.init_node("nodeexample", anonymous=True)

    n = Node()
    n.example_function()

    rospy.spin()
