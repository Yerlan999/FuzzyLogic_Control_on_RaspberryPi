import time
import RPi.GPIO as GPIO
from utilities import *
from MotionControl import *


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
            norm_dist = custom_normalize(weighted_distance, [0, 400], [0, 1])

            # Feed into FLS
            fuzz_val_mot1 = get_fuzzy_value(norm_dist, 1)
            fuzz_val_mot2 = get_fuzzy_value(norm_dist, 2)

            # Normalize output values to match up with PWM range
            norm_speed_mot1 = custom_normalize(float(fuzz_val_mot1), [0, 1], [0, 100])
            norm_speed_mot2 = custom_normalize(float(fuzz_val_mot2), [0, 1], [0, 100])

            # Move motors according to Fuzzy Logic

            print(weighted_distance, norm_speed_mot1, norm_speed_mot2)

            #move_motor(1, float(norm_speed_mot1))
            #move_motor(2, float(norm_speed_mot2))


            #time.sleep(0.01)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Process has been stopped by User")
        GPIO.cleanup()
