import RPi.GPIO as GPIO


# Motor-1`s PIN constants
ENA = 32
IN1 = 29
IN2 = 31

# Motor-2`s PIN constants
ENB = 33
IN3 = 11
IN4 = 13


ena_pwm = GPIO.PWM(ENA, 1000)  # create PWM instance with frequency
enb_pwm = GPIO.PWM(ENB, 1000)
ena_pwm.start(0)  # start PWM of required Duty Cycle
enb_pwm.start(0)


def move_motor(motor, speed, reverse=False):

    if motor == 1:
        if reverse:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        ena_pwm.ChangeDutyCycle(speed)

    if motor == 2:
        if reverse:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        enb_pwm.ChangeDutyCycle(speed)


def move_motors(speed, reverse=False):

    if reverse:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        ena_pwm.ChangeDutyCycle(speed)
        enb_pwm.ChangeDutyCycle(speed)

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    ena_pwm.ChangeDutyCycle(speed)
    enb_pwm.ChangeDutyCycle(speed)
