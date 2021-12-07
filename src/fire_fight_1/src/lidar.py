#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan


import sys, select, termios, tty
import time

import sympy as sym
from sympy.core.symbol import symbols

# ang_1 = symbols('ang_1')
# ang_2 = symbols('ang_2')
# ang_3 = symbols('ang_3')
l_1 = 25.4
l_2 = 16
l_3 = 16






msg = """
Control Your Baby!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
Arm movement:
   a    s    d (a-first link, s- second link , d-end effector)

space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""

moveBindings = {
        'i':(-1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(1,0),
        '.':(-1,1),
        'm':(-1,-1),
             
           }

# speedBindings={
#         'q':(1.1,1.1),
#         'z':(.9,.9),
#         'w':(1.1,1),
#         'x':(.9,1),
#         'e':(1,1.1),
#         'c':(1,.9),
#           }

armBindings={
    'q':(0.01, 0),
    'w':(-0.01, 0),
    'a':(0.01,0),
    's':(-0.01,0),
    'z':(0.01,0),
    'x':(-0.01,0),
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = 8
turn = 0.5
ang3 = 0
ang2=0
ang1=0
# ang_1 = ang1-0.7
l = 10

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

def callback(msg):
    global l
    l  = msg.ranges[6]
    return l

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('teleop')

    pub_right = rospy.Publisher('/fire_fight_1/front_steerR_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    pub_left = rospy.Publisher('/fire_fight_1/front_steerL_position_controller/command', Float64, queue_size=10)
    pub_moveL = rospy.Publisher('/fire_fight_1/rear_wheelL_velocity_controller/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
    pub_moveR = rospy.Publisher('/fire_fight_1/rear_wheelR_velocity_controller/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
    pub_arm3 = rospy.Publisher('/fire_fight_1/third_arm_controller/command', Float64, queue_size=10) #adding the publisher for third_arm_controller
    pub_arm2 = rospy.Publisher('/fire_fight_1/second_arm_controller/command', Float64, queue_size=10)
    pub_arm1 = rospy.Publisher('/fire_fight_1/first_arm_controller/command', Float64, queue_size=10)
    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print(msg)
        print(vels(speed,turn))
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            # elif key in speedBindings.keys():
            #     speed = speed * speedBindings[key][0]
            #     turn = turn * speedBindings[key][1]
            #     count = 0
            
            elif key in armBindings.keys():
                if key=='q':
                    ang3 = ang3 + armBindings[key][0]
                    if ang3>1.57:
                        ang3=1.57
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57)
                elif key=='w':
                    ang3=ang3+armBindings[key][0]
                    if ang3<-1.57:
                        ang3=-1.57
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57)
                elif key=='a':
                    ang2=ang2+armBindings[key][0]
                    if ang2>1.57:
                        ang2=1.57
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57)
                elif key=='s':
                    ang2=ang2+armBindings[key][0]
                    if ang2<-1.57:
                        ang2=-1.57
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57) 
                elif key=='z':
                    ang1=ang1+armBindings[key][0]
                    if ang1>6.28:
                        ang1=6.28
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57)
                elif key=='x':
                    ang1=ang1+armBindings[key][0]
                    if ang3<0:
                        ang3=0
                    print('End effector angle: ', (ang3*90)/1.57)
                    print('Arm-2 angle is: ', (ang2*90)/1.57)
                    print('Arm-1 angle is: ', (ang1*90)/1.57)                             
                # ang2= ang2+ armBindings[key][0]
                # print(ang2)

                # turn = turn * speedBindings[key][1]
                count = 0

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break
            


            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            rospy.Subscriber("/fire_fight_1/scan", LaserScan, callback)
            
            

            

            if (l>1):
                print('Safe zone')
                pub_right.publish(-control_turn)
                pub_left.publish(-control_turn)
                pub_moveL.publish(-control_speed)
                pub_moveR.publish(control_speed)
                pub_arm3.publish(ang3)
                pub_arm2.publish(-ang2)
                pub_arm1.publish(ang1)
                # thet = {ang_1:ang1, ang_2:ang2, ang_3:ang3}
                X = (l_2*sym.sin(ang2) + l_3*(sym.sin(ang2+ang3)))*sym.cos(ang1)
                Y = (l_2*sym.sin(ang2) + l_3*(sym.sin(ang2+ang3)))*sym.sin(ang1)
                Z = l_1 + l_2*sym.cos(ang2) + l_3*sym.cos(ang3 + ang2)
                
                print('the value of x: ', X)
                print('the value of y: ', Y)
                print('the value of z is: ', Z)

            else:
                print('stopped')
                pub_right.publish(0)
                pub_left.publish(0)
                while(l<1.1):
                    pub_moveL.publish(-2)
                    pub_moveR.publish(2)
                   
                    print('Too close')
                
                control_speed=0
                pub_moveL.publish(-control_speed)
                pub_moveR.publish(control_speed)
                print('Safe zone')
                ang3=1
                ang2=-1
                ang1=0.7
                pub_arm3.publish(ang3)
                pub_arm2.publish(ang2)
                pub_arm1.publish(ang1)
                # thet = {ang_1:ang1, ang_2:ang2, ang_3:ang3}
                # print(thet)
                # print('the value of x: ', x.subs(thet))
                # print('the value of y: ', y.subs(thet))
                # print('the value of z is: ', x.subs(thet))
                print('extinguishing in progress')
                time.sleep(10)
                print('fire extinguished')
                time.sleep(5)
                ang3=0
                ang2=0
                ang1=0
                 
                            
                
            

           
           


    except KeyboardInterrupt as e:
        print(e)
        

    # finally:
    #     pub_right.publish(control_turn)
    #     pub_left.publish(control_turn)
    #     pub_moveL.publish(control_speed)
    #     pub_moveR.publish(control_speed)
    #     pub_arm3.publish(ang3)
    #     pub_arm2.publish(ang2)
    #     pub_arm1.publish(ang1)
        # twist = Twist()
        # twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        # twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        # pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)