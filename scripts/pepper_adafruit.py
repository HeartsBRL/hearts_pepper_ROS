#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Int32


class PepperAdafruit():

    def __init__(self):
        self.pepper_say = rospy.Publisher('pepper/say', String, queue_size=10)

        rospy.Subscriber("adafruit/cmd", String, self.adafruit_callback)

    def adafruit_callback(self, data):

        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        if(data.data):
            routine = data.data
            rospy.loginfo("Adafruit Trigger")

            if(data.data == "BRL_WeMo_On"):
                    self.pepper_say.publish("Polly has put the kettle on, we'll all have tea!")
            elif(data.data == "BRL_WeMo_Off"):
                    self.pepper_say.publish("Sukey has turned it off again.")
                    time.sleep(4)
                    self.pepper_say.publish("Does that mean we're going to have iced tea?")
    def pepper_adafruit(self):

        rate = rospy.Rate(10)
        # spin() simply keeps python from exiting until this node is stopped
        while not rospy.is_shutdown():
            #rospy.spinOnce()

            rate.sleep()

if __name__ == '__main__':

    rospy.init_node('pepper_adafruit', anonymous=True)
    pa = PepperAdafruit()
    pa.pepper_adafruit()
    rospy.spin()
