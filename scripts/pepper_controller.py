#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Int32

routine = 0
subroutine = 0
kettleFlag = 0
location_list = ["Home", "Sofa", "Kitchen", "My Armchair"]
cmd_list = ["disengage", "engage"]

def fridge_callback(data):
    global routine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data == 1):
        routine = 1
        rospy.loginfo("Fridge open 1")

def med_callback(data):
    global routine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data == 1):
        routine = 2
        rospy.loginfo("Med open 1")
        
def fdoor_callback(data):
    global routine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data == 1):
        routine = 3
        rospy.loginfo("Front Door open 1")

def cup_callback(data):
    global routine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data == 1):
        routine = 4
        rospy.loginfo("Cup Door open 1")

def pepperspeech_callback(data):
    global routine
    global subroutine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data):
        subroutine = data.data
        rospy.loginfo("Pepper Trigger")

def alexa_callback(data):
    global routine
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if(data.data):
        routine = data.data
        rospy.loginfo("Alexa Trigger")

def pepper_controller():

    global routine
    global subroutine
    global kettleFlag

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    pepper_say = rospy.Publisher('pepper/say', String, queue_size=10)
    pepper_go = rospy.Publisher('pepper/go', String, queue_size=10)
    pepper_cmd = rospy.Publisher('pepper/cmd', String, queue_size=10)

    rospy.init_node('pepper_controller', anonymous=True)

    rospy.Subscriber("cb/kitchen/fridge/binary", Int32, fridge_callback)
    rospy.Subscriber("cb/bedroom/meddrawer/binary", Int32, med_callback)
    rospy.Subscriber("cb/livingroom/frontdoor/binary", Int32, fdoor_callback)
    rospy.Subscriber("cb/kitchen/slidingdoor/binary", Int32, cup_callback)

    rospy.Subscriber("pepper/speech", String, pepperspeech_callback)
    rospy.Subscriber("alexa/cmd", String, alexa_callback)

    rate = rospy.Rate(10)
    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.is_shutdown():
        #rospy.spinOnce()

        if routine == 0:
             pass        
        elif routine == 1:
            pepper_cmd.publish("disengage")
            rospy.loginfo("Fridge open 2")
            pepper_go.publish("Kitchen")
            time.sleep(1)
            pepper_say.publish("The fridge is open.")
            time.sleep(6)
            pepper_say.publish("Lucy left you some chicken soup - you could heat that in the microwave.")
            routine = 0
            pepper_cmd.publish("engage")
        elif routine == 2:
            pepper_cmd.publish("disengage")
            rospy.loginfo("Med open 2")
            pepper_go.publish("My Armchair")
            time.sleep(1)
            pepper_say.publish("The medicine drawer in the living room has been opened.")
            time.sleep(8)
            pepper_say.publish("That medicine should not be taken on an empty stomach.")
            routine = 0
            pepper_cmd.publish("engage")
        elif routine == 3:
            pepper_cmd.publish("disengage")
            rospy.loginfo("Front door open 2")
            pepper_say.publish("Attention, the front door is open.")
            routine = 0
            pepper_cmd.publish("engage")

        elif routine == 4:
            #pepper_cmd.publish("disengage")
            rospy.loginfo("cup door open 2")
            if(kettleFlag == 0):
                    pepper_say.publish("You've opened the cupboard, did you want a cup of tea?")
                    time.sleep(6)
                    pepper_say.publish("Ok, make sure there's water in the kettle before turning it on.")
                    time.sleep(2)
                    kettleFlag = 1
            else:
                    pepper_say.publish("You've opened the cupboard again.")
                    time.sleep(5)
                    kettleFlag = 0
            routine = 0

        else:
            if routine in location_list:
                    pepper_say.publish("Heading to " + routine)
                    time.sleep(2)
                    pepper_go.publish(routine)
            elif routine in cmd_list:
                    pepper_say.publish(routine + "ing listening mode")
                    pepper_cmd.publish(routine)
                    time.sleep(1)
            else:
                    pepper_say.publish("Sorry, I'm not sure where the " + routine + " is.")
            routine = 0

        rate.sleep()

if __name__ == '__main__':
    pepper_controller()
