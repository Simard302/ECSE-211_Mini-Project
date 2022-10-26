#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
import brickpi3
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

TOUCH_SENSOR1 = TouchSensor(1)
TOUCH_SENSOR2 = TouchSensor(2)
TOUCH_SENSOR3 = TouchSensor(3)
TOUCH_SENSOR4 = TouchSensor(4)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time
pitches = ['A5', 'E5', 'C5', 'D5']

def play_sound(num):
    "Play a single note."
    print(pitches[num-1])
    SOUND = sound.Sound(duration=0.5, pitch=pitches[num-1], volume=75 )
    SOUND.play()
    print('\tstarted')
    SOUND.wait_done()
    print('\tended')


def play_sound_on_button_press():
    
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            if TOUCH_SENSOR1.is_pressed() != 0:
                play_sound(1)
            elif TOUCH_SENSOR2.is_pressed() != 0:
                play_sound(2)
            elif TOUCH_SENSOR3.is_pressed() != 0:
                play_sound(3)
            elif TOUCH_SENSOR4.is_pressed() != 0:
                play_sound(4)
    except BaseException as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(str(e))
        exit()


if __name__=='__main__':
    #play_sound()

    # TODO Implement this function
    play_sound_on_button_press()
