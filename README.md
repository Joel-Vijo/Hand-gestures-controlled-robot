# Hand-gestures-controlled-robot
Controlling and simulating the turtlebot3 in gazebo using hand gestures 

## Packages/Dependencies
Ubuntu OS\
Corresponding version of ROS(Robot Operating System)-http://wiki.ros.org/ROS/Installation \
Gazebo\
Turtlebot3-https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation \
Hand gesture detection-https://github.com/Joel-Vijo/Indian-Sign-language-detection.git


## Working
The turtlebot3 package is cloned. In the python file, we import all the required packages. We then create a ros publisher to publish the twist message in the rostopic cmd_vel. A maximum limit is set for the turtlebot3 models linear and angular velocity. The code used in indian sign language detection is used to detect the hand gestures. Then based on each corresponding gesture the change in linear or angular velocity is made

## Gestures used
5: increase linear velocity \
6: decrease linear velocity(when it becomes negative,robot will move backwards) \
2: increase angular velocity(left) \
9: decrease angular velocity (when negative,it will rotate right) \
0 : force stop

## Demo
In Turtlebot3 world \
![ezgif com-gif-maker](https://user-images.githubusercontent.com/87753623/137074674-52b90297-9441-4da7-aded-31dcc9280c01.gif)\

In Empty world \
![ezgif com-gif-maker(1)](https://user-images.githubusercontent.com/87753623/137356247-987261f4-7ad3-4d86-95dd-822b8a60131b.gif)

