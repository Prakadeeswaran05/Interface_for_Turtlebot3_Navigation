#!/usr/bin/env python  
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point,Twist
from std_msgs.msg import String
from visualization_msgs.msg import Marker,MarkerArray
import Tkinter as tk
import time
root = tk.Tk()
root.title("Navigation")
cmd=Twist()
marker = Marker()

l=[['Room1',(-6.26,-2.07)],['Room2',(-3.18,3.9)],['Room3',(3.02880191803,2.02200937271)],['Room4',(5.79,-4.43)]]	


def forward():
        
        cmd.linear.x=0.5
        cmd.linear.y=0.0
        cmd.linear.z=0.0

        cmd.angular.x=0.0
        cmd.angular.y=0.0
        cmd.angular.z=0.0
        pub.publish(cmd)

def backward():
        
        cmd.linear.x=-0.5
        cmd.linear.y=0.0
        cmd.linear.z=0.0

        cmd.angular.x=0.0
        cmd.angular.y=0.0
        cmd.angular.z=0.0
        pub.publish(cmd)

def right_turn():
       
        cmd.linear.x=0.0
        cmd.linear.y=0.0
        cmd.linear.z=0.0

        cmd.angular.x=0.0
        cmd.angular.y=0.0
        cmd.angular.z=0.5
        pub.publish(cmd)

def left_turn():
        
        cmd.linear.x=0.0
        cmd.linear.y=0.0
        cmd.linear.z=0.0

        cmd.angular.x=0.0
        cmd.angular.y=0.0
        cmd.angular.z=-0.5
        pub.publish(cmd)

def stop():
        cmd=Twist()
        pub.publish(cmd)

def cancel_callback(msg):
        global to_cancel
        to_cancel=msg.data

def move_to_goal(x,y,single_goal,goal_location):
        

        def wrapper(xGoal=x,yGoal=y,goal_loc=goal_location):
                
                global ac
                global to_cancel
                #define a client for to send goal requests to the move_base server through a SimpleActionClient
                ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

                #wait for the action server to come up
                while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
                         rospy.loginfo("Waiting for the move_base action server to come up")

                
                goal = MoveBaseGoal()
                
                
                #set up the frame parameters
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()

                # moving towards the goal*/

                goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
                goal.target_pose.pose.orientation.x = 0.0
                goal.target_pose.pose.orientation.y = 0.0
                goal.target_pose.pose.orientation.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0

                rospy.loginfo("Started next journey")
                ac.send_goal(goal,feedback_cb=callback_active)

                ac.wait_for_result(rospy.Duration(60))

                if(ac.get_state() ==  GoalStatus.SUCCEEDED):
                        print("I am now at {}".format(goal_loc))
                        # marker.id = 0
                        # marker.action = Marker.DELETEALL
                       
                        # marker_pub.publish(marker)
                        return True

                else:
                        rospy.loginfo("The robot failed to reach the destination")
                        to_cancel='ok'
                        # marker.id = 0
                        # marker.action = Marker.DELETEALL
                       
                        # marker_pub.publish(marker)
                        return False

        if single_goal:
                return wrapper
        else:
                return wrapper(x,y,goal_location)
def callback_active(feedback):        

        try:       
                        
                if to_cancel=='cancel_one_goal' and ac.get_state()!=2:
                        ac.cancel_goal()
                       

                       
                elif to_cancel=='cancel_all_goals' and ac.get_state()!=2:
                        for i in range(len(l)):
                                ac.cancel_goal()
                                time.sleep(2)
         
                      
        except:
               pass
       
                

                                        
def multi_goal():
        #print('going innnnnn')
        for goal in l:
                goal_location=goal[0]
                x,y=goal[1]
                move_to_goal(x,y,False,goal_location)

def publish_location():
        for i in range (len(l)):
           
                marker.header.frame_id = "map"
                marker.header.stamp = rospy.Time.now()
                marker.id = i
                
                marker.action = Marker.ADD
                marker.type = Marker.TEXT_VIEW_FACING
                marker.text=l[i][0]
                marker.pose.position.x =l[i][1][0]
                marker.pose.position.y = l[i][1][1]
                marker.pose.orientation.x = 0.0
                marker.pose.orientation.y = 0.0
                marker.pose.orientation.z = 0.0
                marker.pose.orientation.w = 1.0

                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.color.a = 1.0

                marker.scale.x = 0.3
                marker.scale.y=0.3
                marker.scale.z=0.3
                
                marker_pub.publish( marker )
        

if __name__ == '__main__':
   rospy.init_node('map_navigation', anonymous=False)
   pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
   marker_pub=rospy.Publisher('/marker_test', Marker, queue_size=10)
   sub=rospy.Subscriber('/goal_cancel',String, cancel_callback)
   rate = rospy.Rate(10)

   

   button1 = tk.Button(root, text='Room1', width=40, command= move_to_goal(-6.26,-2.07,True,goal_location='Room1'))
   button1.pack()
   button2 = tk.Button(root, text='Room2', width=40, command= move_to_goal(-3.18,3.9,True,goal_location='Room2'))
   button2.pack()
   button3 = tk.Button(root, text='Room3', width=40, command= move_to_goal(3.02880191803,2.02200937271,True,goal_location='Room3'))
   button3.pack()
   button4 = tk.Button(root, text='Room4', width=40, command= move_to_goal(5.79,-4.43,True,goal_location='Room4'))
   button4.pack()
   button5 = tk.Button(root, text='Surveillance Mode', width=40, command=multi_goal)
   button5.pack()
   button6 = tk.Button(root, text='Go Forward', width=40, command=forward)
   button6.pack()
   button7 = tk.Button(root, text='Go Backward', width=40, command=backward)
   button7.pack()
   button8 = tk.Button(root, text='Turn Right', width=40, command=right_turn)
   button8.pack()
   button9 = tk.Button(root, text='Turn Left', width=40, command=left_turn)
   button9.pack()
   button10 = tk.Button(root, text='Stop', width=40, command=stop)
   button10.pack()
   button11 = tk.Button(root, text='Publish Locations', width=40, command=publish_location)
   button11.pack()

   
   
   root.mainloop()
   rospy.spin()
