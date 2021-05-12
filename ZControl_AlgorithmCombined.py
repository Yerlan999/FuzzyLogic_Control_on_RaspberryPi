import time
import RPi.GPIO as GPIO
from utilities import *
from ZMotionControl import *


old_distance = 0

if __name__ == '__main__':
    try:
        while True:

            # Get distance value from Ultra Sonic Sensor
            new_distance = get_distance()
            if new_distance > 400:
                new_distance = old_distance
            new_distance = (new_distance + old_distance)/2
            weighted_distance = round((new_distance*0.1 + old_distance*0.9), 2)
            old_distance = weighted_distance

            time.sleep(0.5)
            # Normalize it to feed into Fuzzy Logic System
            norm_dist1 = custom_normalize(weighted_distance, [0, 400], [-1, 1])
            norm_dist2 = custom_normalize(weighted_distance, [0, 400], [-2, 2])

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
