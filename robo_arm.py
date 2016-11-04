#---Control servos in robotic arm with xbox controller---#
import pygame, RPi.GPIO as gpio, time

#control update frequency
CLOCK = pygame.time.Clock()
clock_speed = 20

#vars for if program running
#and if joystick connected
joystick_connect = True
running = True

#used to end program
def stop():
    for i in range(0, len(servos)):
        servos[i].stop()
    pygame.quit()
    print('clean exit')

#convert a value to degrees, 0-180
def convert(x):
    return ((1.0/18.0)*x+3)

def reset():
    for i in range(0, len(pins)):
        servos[i].ChangeDutyCycle(convert(start_pos[i]))
    
#initailize the pygame library
pygame.init()

#use first joystick connected since only
#one xbox remote is used
joystick = pygame.joystick.Joystick(0)
#initailize joystick
joystick.init()

#initailize GPIO
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#array to hold pin numbers
pins = [21,16,12,23,25,18]
#array of servos
servos = []

#increment variable
start_pos = [-15, 120, 15, 120, 35, 150]
servo_pos = [-15, 120, 15, 120, 35, 150]

#loop through all pins
#setup pins for output mode
#add pin to servo array
#start servo
for i in range(0, len(pins)):
    gpio.setup(pins[i], gpio.OUT)
    servos.append(gpio.PWM(pins[i],50))

servos[0].start(convert(servo_pos[0]))
servos[1].start(convert(servo_pos[1]))
servos[2].start(convert(servo_pos[2]))
servos[3].start(convert(servo_pos[3]))
servos[4].start(convert(servo_pos[4]))
servos[5].start(convert(servo_pos[5]))
    
#limits for servos
UPPER = 180
LOWER = 3

#BOOOLS for movement
base_mv = False
base_mv_opp = False
shoulder_mv = False
shoulder_mv_opp = False
elbow_mv = False
elbow_mv_opp = False
swivel_mv = False
swivel_mv_opp = False
wrist_mv = False
wrist_mv_opp = False
gripper_mv = False
gripper_mv_opp = False

#increment amounts
b_mv = 3
s_mv = 5
e_mv = 5
sw_mv = 5
w_mv = 5
g_mv = 5
'''
servo:
    0 - base
    1 - shoulders
    2 - elbow
    3 - swivel
    4 - wrist
    5 - gripper
'''
#run until user decides to quit
while(running):
    # User did something, this applies to keyboard or
    #joystick
    for event in pygame.event.get(): 
        
        # Check if anything on joystick changed   
        if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:

            #Control swivel base
            #Top left axis, left direction
            #does not allow user to go past limits
            if joystick.get_axis(0) > .9:
                base_mv = True
            elif joystick.get_axis(0) < -.9:
                base_mv_opp = True
            else:
                base_mv = False
                base_mv_opp = False

            #Shoulders - left stick, up/down
            if joystick.get_axis(1) < -.9:
                shoulder_mv = True
            elif joystick.get_axis(1) > .9:
                shoulder_mv_opp = True
            else:
                shoulder_mv = False
                shoulder_mv_opp = False

            #elbow - right stick, up/down
            if joystick.get_axis(4) < -.5:
                elbow_mv = True
            elif joystick.get_axis(4) > .5:
                elbow_mv_opp = True
            else:
                elbow_mv = False
                elbow_mv_opp = False

            #wrist joint - A and Y, A down Y up
            if joystick.get_button(0):
                swivel_mv = True
            elif joystick.get_button(3):
                swivel_mv_opp = True
            else:
                swivel_mv = False
                swivel_mv_opp = False
                

            #wrist swivel - RB and LB, RB left (CCW) LB right (CW)
            if joystick.get_button(5):
                wrist_mv = True
            elif joystick.get_button(4):
                wrist_mv_opp = True
            else:
                wrist_mv = False
                wrist_mv_opp = False

            #gripper - Left trigger open, right trigger close
            if joystick.get_axis(2) < -.5:
                gripper_mv = True
            elif joystick.get_axis(5) < -.5:
                gripper_mv_opp = True
            else:
                gripper_mv = False
                gripper_mv_opp = False
            
            #exit program if start button pressed
            if joystick.get_button(7):
                running = False
                
    #move base
    if base_mv and servo_pos[0] <= 100:
        servo_pos[0] += b_mv
        servos[0].ChangeDutyCycle(convert(servo_pos[0]))
    elif base_mv_opp and servo_pos[0] >= -15:
        servo_pos[0] -= b_mv
        servos[0].ChangeDutyCycle(convert(servo_pos[0]))

    #Shoulders - left stick, up/down
    if shoulder_mv and servo_pos[1] <= 130:
        servo_pos[1] += s_mv
        servos[1].ChangeDutyCycle(convert(servo_pos[1]))
    elif shoulder_mv_opp and servo_pos[1] >= 0:
        servo_pos[1] -= s_mv
        servos[1].ChangeDutyCycle(convert(servo_pos[1]))

    #elbow - right stick, up/down
    if elbow_mv and servo_pos[2] <= 100:
        servo_pos[2] += e_mv
        servos[2].ChangeDutyCycle(convert(servo_pos[2]))
    elif elbow_mv_opp and servo_pos[2] >= 0:
        servo_pos[2] -= e_mv
        servos[2].ChangeDutyCycle(convert(servo_pos[2]))

    #wrist joint - A and Y, A down Y up
    if swivel_mv and servo_pos[3] <= 170:
        servo_pos[3] += sw_mv
        servos[3].ChangeDutyCycle(convert(servo_pos[3]))
    elif swivel_mv_opp and servo_pos[3] >= 10:
        servo_pos[3] -= sw_mv
        servos[3].ChangeDutyCycle(convert(servo_pos[3]))

    #wrist swivel - RB and LB, RB left (CCW) LB right (CW)
    if wrist_mv and servo_pos[4] <= 180:
        servo_pos[4] += w_mv
        servos[4].ChangeDutyCycle(convert(servo_pos[4]))
    elif wrist_mv_opp and servo_pos[4] >= 0:
        servo_pos[4] -= w_mv
        servos[4].ChangeDutyCycle(convert(servo_pos[4]))

    #gripper - Left trigger open, right trigger close
    if gripper_mv and servo_pos[5] <= 170:
        servo_pos[5] += g_mv
        servos[5].ChangeDutyCycle(convert(servo_pos[5]))
    elif gripper_mv_opp and servo_pos[5] >= 0:
        servo_pos[5] -= g_mv
        servos[5].ChangeDutyCycle(convert(servo_pos[5]))

    
    #set clock speed to limit cpu usage
    CLOCK.tick(clock_speed)
    
#end program
stop()

