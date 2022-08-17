import RPi.GPIO as GPIO
import time
import thingspeak
import os
from dotenv import load_dotenv

segments = [18, 22, 32, 36, 38, 37, 31, 29]    #GPIO 24, 25, 12, 16, 26, 6, 5
digits = [15, 33, 35, 40]
digit1 = 15    #7-seg pin 12, GPIO 22
digit2 = 33    #7-seg pin 9, GPIO 13
digit3 = 35    #7-seg pin 8, GPIO 19
digit4 = 40    #7-seg pin 6, GPIO 21
IR = 11
switch = 7
led = 12
buzzer = 13

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(segments, GPIO.OUT, initial=GPIO.LOW)    #toggle all segments
    GPIO.setup(digits, GPIO.OUT, initial=GPIO.HIGH)    #toggle all digits
    GPIO.setup(IR, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #detect IR sensor signal    
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)
    GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)    #sets up buzzer
   
#Under here is the code for thingspeak
# Load environment variables from our .env file into working memory
load_dotenv()

# Set environment variables to global variables (not best practice)
nerfgun_channel_id = os.getenv('nerfgun_channel')
write_key = os.getenv('write_key')

# Setup the different fields, for use in the channel
shot_count_field = os.getenv('shot_count_field')
magazine_change_field = os.getenv('magazine_change_field')
jam_door_field = os.getenv('jam_door_field')

# Mean time between failure might be tricky, therefore not yet implemented
nerfgun_channel = thingspeak.Channel(id=nerfgun_channel_id, api_key=write_key)

def resetValues():
    global shot_count
    global magazineChanges
    global currentNumberOfJams
    shot_count = 0
    magazineChanges = 0
    currentNumberOfJams = 0
 
    """
    bit dec  seg
    0   1    bottom left
    1   2    bottom
    2   4    dot point (decimal)
    3   8    bottom right
    4   16   middle
    5   32   top right
    6   64   top left
    7   128  top
    """
    
numbers = [
0b00010100,
0b11010111,
0b01001100,
0b01000101,
0b10000111,
0b00100101,
0b00100100,
0b01010111,
0b00000100,
0b00000101]
