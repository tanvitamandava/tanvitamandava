import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

BLYNK_AUTH_TOKEN = 'J6-T23_NOh6YHXH-Ee7jMFF2CjGDv_pF'

led1 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.output(led1,GPIO.HIGH)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Led control through V0 virtual pin
@blynk.on("V4")
def v0_write_handler(value):
#    global led_switch
    if int(value[0]) != 0:
        GPIO.output(led1, GPIO.HIGH)
        print('Locked')
    else:
        GPIO.output(led1, GPIO.LOW)
        print('Unlocked')

# Led control through V0 virtual pin
@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk") 

while True:
    blynk.run()