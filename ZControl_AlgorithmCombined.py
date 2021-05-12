import RPi.GPIO as GPIO
from dc_motors import *
from ultra_sonic import *
from ZMotionControl import *
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
            norm_dist1 = custom_normalize(distance, [0, 400], [-1, 1])
            norm_dist2 = custom_normalize(distance, [0, 400], [-2, 2])

            # Feed into FLS
            fuzz_val_mot = get_fuzzy_value(norm_dist1, norm_dist1, norm_dist2)

            # Normalize output values to match up with PWM range
            norm_speed_mot = custom_normalize(fuzz_val_mot, [-1, 1], [0, 100])

            # Move motors according to Fuzzy Logic
            if fuzz_val_mot < 0:
                move_motor(1, norm_speed_mot, reverse=True)
            else:
                move_motor(1, norm_speed_mot)

            time.sleep(0.01)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Process has been stopped by User")
        GPIO.cleanup()
