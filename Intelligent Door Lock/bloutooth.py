from bluedot import BlueDot
from gpiozero import LED
import time

bd = BlueDot() 
led = LED (4)
led.on()

while True:
	bd.wait_for_press()
	led.off()
	time.sleep(5)
	led.on()