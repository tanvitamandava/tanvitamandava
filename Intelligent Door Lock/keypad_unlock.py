import RPi.GPIO as GPIO
import time

R1 = 29
R2 = 31
R3 = 33
R4 = 35

C1 = 32
C2 = 36
C3 = 38
C4 = 40

OUTPUT_PIN = 7  # Use GPIO pin 7 for the output
RED_PIN = 13
GREEN_PIN = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(OUTPUT_PIN, GPIO.OUT)  # Set GPIO pin 7 as output
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)


keypadPressed = -1
input_value = ""

def keypadCallback(channel):
    global keypadPressed

    if keypadPressed == -1:
        keypadPressed = channel

GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

def setAllLines(state):
    GPIO.output(R1, state)
    GPIO.output(R2, state)
    GPIO.output(R3, state)
    GPIO.output(R4, state)

def specialKeyPress():
    global input_value
    pressed = False

    GPIO.output(R3, GPIO.HIGH)
    if GPIO.input(C4) == 1:
        print("Input reset")
        pressed = True

    GPIO.output(R3, GPIO.LOW)
    GPIO.output(R1, GPIO.HIGH)

    if not pressed and GPIO.input(C4) == 1:
        print("Your entered value is " + input_value)
        if input_value == "7015":
            print("Unlocked")
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            GPIO.output(OUTPUT_PIN, GPIO.LOW)  # Turn on the output
            time.sleep(5)
            GPIO.output(GREEN_PIN, GPIO.LOW)
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)
        else:
            print("Wrong Password")
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.LOW)
            time.sleep(0.2) 
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(RED_PIN, GPIO.LOW)

            
       
        pressed = True

    GPIO.output(R1, GPIO.LOW)

    if pressed:
        input_value = ""

    return pressed

def printCharacter(row, character):
    global input_value
    GPIO.output(row, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        input_value = input_value + character[0]
    if GPIO.input(C2) == 1:
        input_value = input_value + character[1]
    if GPIO.input(C3) == 1:
        input_value = input_value + character[2]
    if GPIO.input(C4) == 1:
        input_value = input_value + character[3]
    GPIO.output(row, GPIO.LOW)

try:
    while True:
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        else:
            if not specialKeyPress():
                printCharacter(R1, ["1", "2", "3", "A"])
                printCharacter(R2, ["4", "5", "6", "B"])
                printCharacter(R3, ["7", "8", "9", "C"])
                printCharacter(R4, ["*", "0", "#", "D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.output(OUTPUT_PIN, GPIO.LOW)  # Turn off the output before exiting
    GPIO.cleanup()
    print("Stopped")