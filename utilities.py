import RPi.GPIO as GPIO
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

# Setting up PIN modes
GPIO.setmode(GPIO.BOARD)  # by physical PIN layout
GPIO.setwarnings(False)  # disable warnings

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)


ena_pwm = GPIO.PWM(ENA, 1000)  # create PWM instance with frequency
enb_pwm = GPIO.PWM(ENB, 1000)
ena_pwm.start(0)  # start PWM of required Duty Cycle
enb_pwm.start(0)



def custom_normalize(to_convert, input_range, output_range):
    """
        Parameters:
            to_convert --> number to convert from input range to output range
            input_range --> list of 2 integer of float items
            output_range --> list of 2 integer of float items
    """
    assert len(input_range) == 2, "Input range should be list of 2 items"
    assert len(output_range) == 2, "Output range should be list of 2 items"
    assert type(to_convert) in [int, float], "Only integer and float is allowed to convert"
    assert output_range[0] < output_range[1], "First range number must be less than second number"
    assert input_range[0] < input_range[1], "First range number must be less than second number"

    for i in input_range + output_range:
        assert type(i) == int or type(i) == float, "Only integers and floats are allowed in range values"

    inp_str, inp_end, out_str, out_end = input_range + output_range

    if to_convert > input_range[1]:
        to_convert = input_range[1]
    if to_convert < input_range[0]:
        to_convert = input_range[0]

    inp_diff = abs(inp_str-inp_end)
    out_diff = abs(out_str-out_end)
    coefficient = inp_diff / out_diff
    print("Coefficient: ", coefficient)


    if inp_str == 0 and out_str == 0:
        return to_convert / coefficient
    if inp_str < 0 and out_str < 0:
        return to_convert / coefficient


    if out_str < 0:
        return to_convert / coefficient - out_end
    if inp_str < 0:
        return to_convert / coefficient + (out_diff/inp_diff)
    if out_str > 0:
        return to_convert / coefficient + out_str




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

    return float(distance)


def move_motor(motor, speed, reverse=False):

    if motor == 1:
        if reverse:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            ena_pwm.ChangeDutyCycle(speed)
        else:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            ena_pwm.ChangeDutyCycle(speed)

    if motor == 2:
        if reverse:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            enb_pwm.ChangeDutyCycle(speed)
        else:
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
    else:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        ena_pwm.ChangeDutyCycle(speed)
        enb_pwm.ChangeDutyCycle(speed)

