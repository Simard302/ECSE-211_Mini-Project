from utils.brick import Motor, TouchSensor, TouchSensor
from utils import sound
import time
from multiprocessing import Process, Thread
import os

touch1 = TouchSensor(1)
touch2 = TouchSensor(2)
touch3 = TouchSensor(3)
touch4 = TouchSensor(4)
kick = Motor("A")
clap = Motor("B")
bpm_setter = Motor("C")


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
        
    print(BPM)
        
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
    "1111":"toggle",
    "0000":"none",
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
def readFlute(is_pressed, index):
    is_pressed[index] = flutes[index].is_pressed()

def drive_flute():
    # Setting up lists for threads and their return values
    is_pressed = [None] * len(flutes)
    threads = [None] * len(flutes)

    # Starting a thread for each input
    for i in range(0, len(flutes)):
        threads[i] = Thread(target=readFlute, args=(is_pressed, i))
        threads[i].start()
    # Merging the threads back into main branch
    # is_pressed is now updated
    for i in range(0, len(flutes)):
        threads[i].join()
    code = "".join(list(map(str, list(map(int, is_pressed)))))
    print(code)

    note = value_map[code]
    if note == "none" or note == "toggle":
        time.sleep(note_duration)
        if note == "toggle": return
        drive_flute()
    print(note)
    SOUND = sound.Sound(duration=note_hold_extra_time*note_duration, pitch=note, volume=flute_vol )
    SOUND.play()
    time.sleep(note_duration)
    drive_flute()
    
if __name__ == "__main__":
    try:
        p2 = Process(target = play_drums)
        p2.start()
        p1 = Process(target = drive_flute)
        p1.start()
        t1 = ("1" if touch1.is_pressed() else "0")
        t2 = ("1" if touch2.is_pressed() else "0")
        t3 = ("1" if touch3.is_pressed() else "0")
        t4 = ("1" if touch4.is_pressed() else "0")
        while (t1+t2+t3+t4 != "1111"):
            t1 = ("1" if touch1.is_pressed() else "0")
            t2 = ("1" if touch2.is_pressed() else "0")
            t3 = ("1" if touch3.is_pressed() else "0")
            t4 = ("1" if touch4.is_pressed() else "0")
            continue
        raise BaseException
        #os.sys('ps aux | grep "^python3 -m thonny" | kill')
    except BaseException as e:
        print(str(e))
        p1.kill()
        p2.kill()
        print("end")
