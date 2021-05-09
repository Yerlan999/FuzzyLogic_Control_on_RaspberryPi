from normalizing_funcs import custom_normalize
import RPi.GPIO as GPIO
from time import sleep
import time


# Ultra sonic distance sensor`s PIN constants
TRIGGER = 18
ECHO = 24

# Motor-1`s PIN constants
ENA = 32
IN1 = 29
IN2 = 31

# Motor-2`s PIN constants
ENB = 33
IN3 = 11
IN4 = 13


# Useful functions needed for the process


def get_distance():
    # set Trigger to HIGH
    GPIO.output(TRIGGER, GPIO.HIGH)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, GPIO.LOW)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def move_motor_1(fuzzy_value):
    pass


# Setting up PIN modes
GPIO.setmode(GPIO.BOARD)          #by physical PIN layout
GPIO.setwarnings(False)           #disable warnings

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)


ena_pwm = GPIO.PWM(ENA, 1000)      #create PWM instance with frequency
enb_pwm = GPIO.PWM(ENB, 1000)
ena_pwm.start(0)                   #start PWM of required Duty Cycle
enb_pwm.start(0)

#pi_pwm.ChangeDutyCycle(duty)



