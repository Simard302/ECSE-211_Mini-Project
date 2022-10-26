import code
from utils.brick import Motor, TouchSensor, TouchSensor
from utils import sound
import time
from multiprocessing import Process
from threading import Thread
import os

touch1 = TouchSensor(1)
touch2 = TouchSensor(2)
touch3 = TouchSensor(3)
touch4 = TouchSensor(4)
kick = Motor("A")
clap = Motor("B")
bpm_setter = Motor("C")

REFRESH_RATE_FREE = 0.05
REFRESH_RATE_HOLD = 0.5
HOLD_TIME = 1

hit_factor = 4 #(min 1.0)
flute_vol = 90
note_duration = 0.1
note_hold_extra_time = 3
drum_pattern = "kkc "

KICK_POWER = 100 #full power kick motor
CLAP_POWER = 100 #full power clap motor

BPM = bpm_setter.get_position() #default value of bpm radial setter (lowest BPM)
SPEED = BPM*6 # Conversion of BPM to Deg --> SPEED = BPM * 360degrees / 60seconds
        
def play_drum(drum):
    #same bit of code as the other function, the idea is to allow BPM changes will the kicks and claps are playing
    BPM = bpm_setter.get_position()
    if(BPM<=60):
        BPM=60

    if(BPM>=200):
        BPM=200
        
    SPEED = BPM*6*hit_factor
    
    kick.set_limits(KICK_POWER, SPEED) #set limit of lower value between max power and speed of kick motor
    clap.set_limits(CLAP_POWER, SPEED) #set limit of lower vlue bwetween max power and speed of clap motor

            
    if(drum=='k'):
        kick.set_position_relative(360)
        time.sleep(360*hit_factor/SPEED)
    elif(drum=='c'):
        clap.set_position_relative(360)
        time.sleep(720*hit_factor/SPEED)
    elif(drum==' '):
        time.sleep(360*hit_factor/SPEED)
    else:
        print("Invalid character")

        
def play_drums():
    #string of notes representing kicks and claps
    for character in drum_pattern:
        play_drum(character)
        #play_note(flute_note)
    play_drums()

flutes = [
    touch1,
    touch2,
    touch3,
    touch4
]
value_map = {
    "0001":"A4",
    "0010":"D5",
    "0011":"B4",
    "0100":"Gb5",
    "0101":"Gb5",
    "0110":"E5",
    "0111":"E5",
    "1000":"A5",
    "1001":"A5",
    "1010":"A5",
    "1011":"A5",
    "1100":"G5",
    "1101":"G5",
    "1110":"G5"
}
def readButton(is_pressed, index):
    is_pressed[index] = flutes[index].is_pressed()

def readFlute():
    # Setting up lists for threads and their return values
    is_pressed = [None] * len(flutes)
    threads = [None] * len(flutes)

    # Starting a thread for each input
    for i in range(0, len(flutes)):
        threads[i] = Thread(target=readButton, args=(is_pressed, i))
        threads[i].start()
    # Merging the threads back into main branch
    # is_pressed is now updated
    for i in range(0, len(flutes)):
        threads[i].join()
    return "".join(list(map(str, list(map(int, is_pressed)))))
    
if __name__ == "__main__":
    drumProc = Process(target = play_drums)
    try:
        while True:
            code = readFlute()

            if code == "1111":
                if drumProc.is_alive():
                    # kill drum processes, break
                    drumProc.kill()
                    break
                else:
                    # Start drum process
                    drumProc.start()
                    time.sleep(HOLD_TIME)
            elif code == "0000":
                time.sleep(REFRESH_RATE_FREE)
            else:
                # play flute sounds
                print(code)
                SOUND = sound.Sound(
                    duration=note_hold_extra_time*note_duration, 
                    pitch=value_map[code], 
                    volume=flute_vol
                )
                SOUND.play()
                time.sleep(max((60/BPM), note_duration))
    except BaseException as e:
        print(str(e))
        if drumProc.is_alive(): drumProc.kill()
        print("end")
