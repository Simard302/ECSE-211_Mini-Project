import code
from utils.brick import Motor, TouchSensor, TouchSensor
from utils.sound import NOTES, gen_wave
import time
from multiprocessing import Process
from threading import Thread
import simpleaudio as sa

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
    # Get BPM from motor position
    BPM = bpm_setter.get_position()
    # Clamp BPM to avoid
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
        # Play individual drum sound
        play_drum(character)
    # Re-loop drumming (recursive)
    play_drums()

def init_waves():
    # Pre-generate all waves for existing notes
    # Makes the sound playing much faster
    note_waves = {}
    for note in value_map.values():
        note_waves[note] = gen_wave(
            note_hold_extra_time*note_duration, 
            flute_vol, 
            NOTES[note], 
            0,0, 0, 0, 1, 0.01, 8000
        )
    return note_waves



flutes = [
    touch1,
    touch2,
    touch3,
    touch4
]
value_map = {
    "0001":"G5",
    "0010":"Gb5",
    "0011":"B4",
    "0100":"E5",
    "0101":"Gb5",
    "0110":"E5",
    "0111":"E5",
    "1000":"D5",
    "1001":"A5",
    "1010":"A5",
    "1011":"A5",
    "1100":"G5",
    "1110":"G5",
    "1101":"G5"
}
def readButton(is_pressed, index):
    is_pressed[index] = flutes[index].is_pressed()

def readFlute():
    # Setting up lists for threads and their return values
    # Pre-allocating space for Thread to reference
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
    # Format the True/False list into 0 and 1's string
    return "".join(list(map(str, list(map(int, is_pressed)))))
    
if __name__ == "__main__":
    waves = init_waves()
    drumProc = Process(target = play_drums)
    player = None
    try:
        while True:
            # Read all flute inputs (threaded)
            code = readFlute()

            if code == "1111":
                if drumProc.is_alive():
                    # kill drum processes, break
                    drumProc.kill()
                    print("Stopping all processes")
                    break
                else:
                    # Start drum process
                    drumProc.start()
                    print("Starting drum")
                    time.sleep(HOLD_TIME)
            elif code == "0000":
                # No buttons pressed, add a time.sleep to slow the while loop
                time.sleep(REFRESH_RATE_FREE)
            else:
                # play flute sounds
                print(code)
                # If sound is already playing, stop it
                if player is not None and player.is_playing():
                    player.stop()
                # Play new sound with pre-generated wave (faster)
                player = sa.play_buffer(waves[value_map[code]], 1, 2, 8000)
                # Sleep for duration of sound
                time.sleep(note_hold_extra_time*note_duration)
    except BaseException as e:
        print(str(e))
        if drumProc.is_alive(): drumProc.kill()
        print("end")
