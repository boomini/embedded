import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 100) 
button_p1=19
button_p2=13
speed = 0.5


def button_callback(channel):
	global light_on 
	print("Button pushed!")
	if channel == button_p1:
		if light_on == False: # LED 불이 꺼져있을때
			GPIO.output(led_pin2,1) 
			GPIO.output(led_pin,0)
			p.start(10) 
			p.ChangeFrequency(262)
			#time.sleep(speed) 
			print("LED ON!")
		else: # LED 불이 켜져있을때
			GPIO.output(led_pin2,0) 
			p.stop() 
			print("LED OFF!")
		light_on = not light_on
	elif channel == button_p2:
		if light_on == False: # LED 불이 꺼져있을때
			GPIO.output(led_pin,1) 
			GPIO.output(led_pin2,0)
			p.start(10) 
			p.ChangeFrequency(294)
			#time.sleep(speed) 
			print("LED ON!")
		else: # LED 불이 켜져있을때
			GPIO.output(led_pin,0) 
			p.stop() 
			print("LED OFF!")
		light_on = not light_on 

	
	
led_pin = 4
led_pin2 = 3
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(button_p1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_p2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
light_on=False
GPIO.add_event_detect(button_p1,GPIO.BOTH,callback=button_callback,bouncetime=1)
GPIO.add_event_detect(button_p2,GPIO.BOTH,callback=button_callback,bouncetime=1)
while 1:
		time.sleep(0.1)
