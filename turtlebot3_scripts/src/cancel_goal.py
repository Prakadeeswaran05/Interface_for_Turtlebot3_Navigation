#!/usr/bin/env python 
import rospy
from std_msgs.msg import String
import Tkinter as tk
root = tk.Tk()
root.title("cancel goal")
def cancel_one_goal():
    pub.publish('cancel_one_goal')

def cancel_all_goals():
    pub.publish('cancel_all_goals')


if __name__ == '__main__':
   rospy.init_node('cancel_goal', anonymous=False)
   pub=rospy.Publisher('/goal_cancel',String, queue_size=10)
   button1 = tk.Button(root, text='Cancel one goal', width=40, command=cancel_one_goal)
   button1.pack()
   button2 = tk.Button(root, text='Cancel all goals', width=40, command=cancel_all_goals)
   button2.pack()
 
   root.mainloop()
   rospy.spin()