import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) ; GPIO.setmode(GPIO.BCM)
trig = 23 ; echo = 24 #센서에 연결한 Trig와 Echo 핀의 핀 번호 설정
print ("start")

GPIO.setup(trig, GPIO.OUT); GPIO.setup(echo, GPIO.IN)  #Trig와 Echo 핀의 출력/입력 설정
GPIO.output(trig, False) #Trig핀의 신호를 0으로 출력
print("Waiting for sensor to settle")

time.sleep(2)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 100) 

speed = 0.1 

try :
	while True :
		GPIO.output(trig, True) # Triger 핀에 펄스신호를 만들기 위해 1 출력
		time.sleep(0.00001) # 10µs 딜레이
		GPIO.output(trig, False)
		
		while GPIO.input(echo) == 0 :
			pulse_start = time.time() # Echo 핀 상승 시간 (펄스가 출력되는 시점)
		while GPIO.input(echo) == 1 :
			pulse_end = time.time() # Echo 핀 하강 시간 (반사되어 돌아온 시점)
			
		pulse_duration = pulse_end - pulse_start # 거리 측정을 위한 식
		distance = pulse_duration * 34300/2
		distance = round(distance, 2)
		print ("Distance : ", distance, "cm")
		if distance<8:
			p.start(10) 
			p.ChangeFrequency(262)
			time.sleep(speed)
			p.stop()
		time.sleep(0.2)
except KeyboardInterrrupt:
	print("Measurement stopped by User")
	GPIO.cleanup()
