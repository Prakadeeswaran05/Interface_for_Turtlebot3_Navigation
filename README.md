# Interface_for_Turtlebot3_Navigation

First clone this repo and paste the turtlebot3_scripts folder alone inside your src.
</br>
Then,
``` 
$ cd ~/catkin_ws/src/
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git -b melodic-devel
$ git clone  https://github.com/ROBOTIS-GIT/turtlebot3.git -b melodic-devel
$ cd ~/catkin_ws && catkin_make
```
After the correct compilation of workspace proceed with installation of simulation packages as shown below.
```
$ cd~/catkin_ws/src/
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
$ cd ~/catkin_ws && catkin_make
```


Finally to test the script follow the steps given below.
</br>
```
roslaunch turtlebot3_gazebo turtlebot3_house.launch 
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/ros1/catkin_ws/src/turtlebot3_scripts/src/tb3map/tb3_house_map.yaml
roslaunch turtlebot3_scripts navigation_commands.launch 
```
Voila! You will see tkinter buttons to do various tasks like navigating to a specific location,cancelling goals,publishing location etc.

<p align="left">
  <img src="navigation_output.gif" />
</p>
</br>
</br>
<p align="left">
