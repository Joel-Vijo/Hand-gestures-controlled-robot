#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist


MAX_LIN_VEL = 0.25
MAX_ANG_VEL = 2.84

LIN_VEL_STEP_SIZE = 0.02
ANG_VEL_STEP_SIZE = 0.01
msg = """
Control Your TurtleBot3!
---------------------------


5: increase linear velocity
6: decrease linear velocity(when it becomes negative,robot will move backwards) 
2: increase angular velocity(left)
9: decrease angular velocity (when negative,it will rotate right)

0 : force stop

esc to quit
"""

e = """
Communications Failed
"""
def vels(linear_vel, angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (linear_vel,angular_vel)

#To make sure the linear velocity does not cross the limit
def checkLinearLimit(vel):
    if vel>MAX_LIN_VEL:
      vel = MAX_LIN_VEL
    elif vel<-MAX_LIN_VEL:
        vel = -MAX_LIN_VEL
    else:
        vel=vel

    return vel

#To make sure the angular velocity does not cross the limit
def checkAngularLimit(vel):
    if vel>MAX_ANG_VEL:
        vel = MAX_ANG_VEL
    elif vel<-MAX_ANG_VEL:
        vel = -MAX_ANG_VEL
    else:
        vel=vel
    return vel

if __name__=="__main__":
    
    rospy.init_node('turtlebot3_hand')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)#creating a publisher
        
    linear_vel   = 0.0
    angular_vel  = 0.0
    cap = cv2.VideoCapture(0)
    target=cv2.imread('hands.png')#input image containing all the gestures
    grey1=cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)
    hsv2 = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
    lower = np.array([10,20,70],dtype=np.uint8)        
    upper = np.array([20,255,255],dtype=np.uint8)

    #getting a thresholded image containing only those pixels having skin color        
    mask2 = cv2.inRange(hsv2, lower, upper)
        


    mask2 = cv2.GaussianBlur(mask2,(3,3),50)#smoothing the image
    c,hierarchy=cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#getting the contours
    cnt2 = sorted(c, key=cv2.contourArea, reverse=True)#sorting the contours based on area

    try:
        print(msg)
        while(1):
            ret, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            grey2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #range of skin color
            lower_skin = np.array([0,50,0],dtype=np.uint8)
            upper_skin = np.array([180,255,255],dtype=np.uint8)
        
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
            #to get a proper thresholded image of the hand
            kernel = np.ones((3,3),np.uint8)
            mask = cv2.dilate(mask,kernel,iterations = 3)
            mask = cv2.GaussianBlur(mask,(3,3),10)

            
        
            contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#geting the contours
        
        
            
            cnt = sorted(contours, key=cv2.contourArea, reverse=True)#sorting the contours in descending order based on area

            #to detect 5
            area=cv2.contourArea(cnt[0])
            frame=cv2.drawContours(frame,[cnt[0]],0,[0,255,0],3)#cnt[0] is the largest contour that is captured by the camera i.e the hand
            font = cv2.FONT_HERSHEY_SIMPLEX
            if (area>30000):
                cv2.putText(frame,str(5),(10,500), font, 4, (0,0,255), 2, cv2.LINE_AA)
                linear_vel = checkLinearLimit(linear_vel + LIN_VEL_STEP_SIZE)
                print(vels(linear_vel,angular_vel))
            for i in range(0,10):
                ret = cv2.matchShapes(cnt[0],cnt2[i],1,0.0)#returns a value after comparing the respective contour of input image with that of our hand
                if(ret<0.09):#lower the value,more similar are the images
                    if(i==2):
                        cv2.putText(frame,str(6),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        linear_vel = checkLinearLimit(linear_vel - LIN_VEL_STEP_SIZE)
                        print(vels(linear_vel,angular_vel))
                        
                    elif(i==1):
                        cv2.putText(frame,str(0),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        linear_vel   = 0.0
                        angular_vel  = 0.0
                        print(vels(linear_vel,angular_vel))
                        
                    elif(i==3):
                        cv2.putText(frame,str(7),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        
                    elif(i==7):
                        cv2.putText(frame,str(1),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        
                    elif(i==4 and area>23950):
                        cv2.putText(frame,str(4),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        
                    elif(i==5 and area<20000):
                        cv2.putText(frame,str(3),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        
                    elif(i==6):
                        cv2.putText(frame,str(8),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        
                    elif(i==8):
                        cv2.putText(frame,str(2),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        angular_vel = checkAngularLimit(angular_vel + ANG_VEL_STEP_SIZE)
                        print(vels(linear_vel,angular_vel))
                        
                    elif(i==0 and area>23000):
                        cv2.putText(frame,str(9),(10,500), font, 4,(0,0,255),2,cv2.LINE_AA)
                        angular_vel = checkAngularLimit(angular_vel - ANG_VEL_STEP_SIZE)
                        print(vels(linear_vel,angular_vel))
                        
                twist = Twist()

                
                twist.linear.x = linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0
                twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = angular_vel

                pub.publish(twist)
            
            cv2.imshow('frame',frame)
            k = cv2.waitKey(5) & 0xFF#to exit from the window
            if k == 27:
                break
    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)