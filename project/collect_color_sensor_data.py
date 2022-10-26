#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY_SEC = 0.01  # seconds of delay between measurements
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(1)
TOUCH_SENSOR = TouchSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    try:
        "Collect color sensor data."
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        # ------
        while(True):
            sleep(DELAY_SEC)
            if (TOUCH_SENSOR.is_pressed()):
                rgb_value = COLOR_SENSOR.get_rgb() #check difference between get_value() and get_rgb()
                print('recorded data')
                sleep(1)
                if (TOUCH_SENSOR.is_pressed()):
                    print('breaking')
                    break
                elif rgb_value is not None: # If None is given, then data collection failed that time
                    print(rgb_value)
                    output_file.write(f"{rgb_value}\n")

    except BaseException:
        print("Exception occurred, exiting...")
        pass
    finally:
        print("Done collecting rgb value samples")
        output_file.close()
        reset_brick()
        exit()


if __name__ == "__main__":
    collect_color_sensor_data()
