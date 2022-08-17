#stuff works, but magazine change counter is weird, it counts right and wrong at random times.
#seems to have been fixed by adding a full second to debounce
from init import *

#Why do we need the next four lines here, and not in init.py? F I X  M E
jamDoorPin = 16
GPIO.setmode(GPIO.BOARD)    # Set GPIO mode to board, just like the rest of code used
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(jamDoorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Set jamDoorPin to use the 10K built-in resistor
GPIO.setup(IR, GPIO.IN, pull_up_down=GPIO.PUD_UP)     #Set beam_pin to use the 10K built-in resistor
currentNumberOfJams = 0
shot_count = 0
magazineChanges = 0
currentNumberOfJams = 0

def jamDoorOpened(self):
        global currentNumberOfJams
        time.sleep(0.005)
        currentNumberOfJams = currentNumberOfJams + 1
        print("Door has been opened, jam detected...")
GPIO.add_event_detect(jamDoorPin, GPIO.FALLING, callback=jamDoorOpened, bouncetime=300)    #needs to see jamDoorOpened
    
def displayNumber(number):    #using the bitmaps, turn every segment on/off to display a number
    for bit, segment in enumerate(segments):
        if ((1<<bit) & number):        #compares bitmap
            GPIO.output(segment, 1)    #turns on
        else:
            GPIO.output(segment, 0)    #turns off
            
def displayDigit(digitToManipulate):
    for other in digits:
        GPIO.output(other, 1)
    GPIO.output(digitToManipulate, 0)
    
def turnOff(firstOff, secondOff):    #turns off unused digits
    GPIO.output(firstOff, 0)
    GPIO.output(secondOff, 0)
    
def stop():    #cleanup protocol
    print("Stopping the coding before something burns down...")
    GPIO.cleanup()
    
def emptyMag():
    looping = True
    while (looping==True):
        if(GPIO.input(switch)==GPIO.HIGH): looping = False    #if the magazine goes out, jump to switch toggle
        numberToDisplay = 10
        print("0") 
        GPIO.output(digit4, 0)
        GPIO.output(digit3, 1)
        displayNumber(numbers[0])
        time.sleep(0.01)    #if it does not blink, it is invisible
        GPIO.output(digit4, 1)
        GPIO.output(digit3, 0)
        displayNumber(numbers[0])
        time.sleep(0.01)

def decrementDisplayIncrementCount(self):    #shot-thingspeak
    global shot_count
    shot_count = shot_count + 1
GPIO.add_event_detect(IR, GPIO.FALLING, callback=decrementDisplayIncrementCount)

def magazineRemoved(self):    #mag-thingspeak
    global magazineChanges
    magazineChanges = magazineChanges + 1
    response = thingspeakSend()
    if (response != 0): resetValues()
GPIO.add_event_detect(switch, GPIO.FALLING, callback=magazineRemoved, bouncetime=1000)

def loop():
    numberToDisplay = 0
    global shot_count
    global magazineChanges
    global currentNumberOfJams
    cycle = False
    
    while True:
        #magazine is in - switch replaces hull sensor for now
        if(GPIO.input(switch)==GPIO.LOW):
            GPIO.output(led, GPIO.HIGH)    #temp led indicator
                
            while(cycle == False):    #making a '10' display
                if(GPIO.input(switch)==GPIO.HIGH): break    #if the magazine goes out, jump to switch toggle
                NumberToDisplay = 10
                print(numberToDisplay)
                GPIO.output(digit4, 0)
                GPIO.output(digit3, 1)
                displayNumber(numbers[1])
                time.sleep(0.01)    #if it does not blink, it is invisible
                GPIO.output(digit4, 1)
                GPIO.output(digit3, 0)
                displayNumber(numbers[0])
                time.sleep(0.01)
                if(GPIO.input(IR)==GPIO.HIGH):
                    cycle = True    #if the IR beam is broken, jump out of the 'multiplexing' loop
                    numberToDisplay = 9
                    displayNumber(numbers[9])
            
            #the IR sensor sends a signal, it has 0.3v (low) output.
            #when the sensor signal is broken, the IR will send a 3v signal (high)
            if(GPIO.input(IR)==GPIO.LOW and numberToDisplay != 0):    #when the IR beam is NOT broken (is continious)
                time.sleep(0.1)    #ROF vs debounce ?
                if(numberToDisplay == 0 and cycle == False):    #count from the top
                    numberToDisplay = 9
                    GPIO.output(digit3, 0)    #if we go from 10 to 9, there is no use for the 3rd digit
                
                elif(GPIO.input(IR)==GPIO.HIGH):    #otherwise, when it is broken
                    GPIO.output(digit3, 0)
                    numberToDisplay = numberToDisplay - 1    #counts down from 10 to 0
                    if(numberToDisplay==5):     #buzz once when at 5 darts left
                        GPIO.output(buzzer, GPIO.HIGH)
                        time.sleep(0.05)
                        GPIO.output(buzzer, GPIO.LOW)
                    if(numberToDisplay==0):    #buzz twice when mag is empty
                        GPIO.output(buzzer, GPIO.HIGH)
                        time.sleep(0.05)
                        GPIO.output(buzzer, GPIO.LOW)
                        time.sleep(0.05)
                        GPIO.output(buzzer, GPIO.HIGH)
                        time.sleep(0.05)
                        GPIO.output(buzzer, GPIO.LOW)
                    
                print("Shots fired: " + str(shot_count))    #prints thingspeak items
                print("Magazine changes: " + str(magazineChanges))
                print("Current number of jams: " + str(currentNumberOfJams))
                displayNumber(numbers[numberToDisplay])
            if(GPIO.input(IR)==GPIO.LOW and numberToDisplay == 0):
                emptyMag()
        #magazine is out
        else:
            GPIO.output(led, GPIO.LOW)
            GPIO.output(digit4, 0)    #turn off the digits we're using.
            GPIO.output(digit3, 0)
            cycle = False    #mag is out, so the cycle starts over
            
def thingspeakSend():    #sending to ThingSpeak
    response = nerfgun_channel.update({shot_count_field: shot_count, magazine_change_field: magazineChanges, jam_door_field: currentNumberOfJams})
    return response

    
if __name__ == "__main__":    #starts the program
    setup()
    print("Starting the counter...")
    try:
        turnOff(digit1, digit2)
        displayNumber(numbers[0])   #what number to display
        resetValues()    #resets thingspeak values
        loop()
    except KeyboardInterrupt:
        stop()
