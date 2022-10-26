from utils.brick import Motor, TouchSensor
import time

KICK_POWER = 100
CLAP_POWER = 100

BPM = 162
SPEED = BPM*6 # Conversion of BPM to Deg --> SPEED = BPM * 360degrees / 60seconds

starter = TouchSensor(1)
touch2 = TouchSensor(2)
touch3 = TouchSensor(3)
touch4 = TouchSensor(4)
kick = Motor("A")
clap = Motor("B")

def play_drums():
    while True:
        while not starter.is_pressed():
            pass
        
        1440/4
        kick.set_position_relative(720)
        time.sleep(720/SPEED)
        #kick.set_position_relative(360)
        clap.set_position_relative(360)
        time.sleep(720/SPEED)
    

if __name__ == "__main__":
    kick.set_limits(KICK_POWER, SPEED)
    clap.set_limits(CLAP_POWER, SPEED)
    play_drums()