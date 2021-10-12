# Hand-gestures-controlled-robot
Controlling and simulating the turtlebot3 in gazebo using hand gestures 

## Packages/Dependencies
Ubuntu OS\
Corresponding version of ROS(Robot Operating System)\
Gazebo\
Turtlebot3-https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation \
Hand gesture detection-https://github.com/Joel-Vijo/Indian-Sign-language-detection.git


## Working
The turtlebot3 package is cloned. In the python file, we import all the required packages. We then create a ros publisher to publish the twist message in the topic cmdvel. A maximum limit is set for the turtlebot3 models linear and angular velocity. The code used in indian sign language detection is used to detect the hand gestures. Then based on each corresponding gesture the change in linear or angular velocity is made
