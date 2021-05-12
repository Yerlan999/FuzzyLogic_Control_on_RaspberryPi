import RPi.GPIO as GPIO
from dc_motors import *
from ultra_sonic import *
from MotionControl import *
from normalizing_funcs import *


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


if __name__ == '__main__':
    try:
        while True:
            # Get distance value from Ultra Sonic Sensor
            distance = get_distance()

            # Normalize it to feed into Fuzzy Logic System
            norm_dist = custom_normalize(distance, [0, 400], [0, 1])

            # Feed into FLS
            fuzz_val_mot1 = get_fuzzy_value(norm_dist, 1)
            fuzz_val_mot2 = get_fuzzy_value(norm_dist, 2)

            # Normalize output values to match up with PWM range
            norm_speed_mot1 = custom_normalize(fuzz_val_mot1, [0, 1], [0, 100])
            norm_speed_mot2 = custom_normalize(fuzz_val_mot2, [0, 1], [0, 100])

            # Move motors according to Fuzzy Logic
            move_motor(1, norm_speed_mot1)
            move_motor(2, norm_speed_mot2)

            time.sleep(0.01)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Process has been stopped by User")
        GPIO.cleanup()
