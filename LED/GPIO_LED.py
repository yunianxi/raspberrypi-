import RPi.GPIO as GPIO
import time

A = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(A,GPIO.OUT)
while 1 :
	GPIO.output(7,1)
	time.sleep(1)
    
GPIO.cleanup()



