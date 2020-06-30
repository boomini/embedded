import smtplib,ssl
import RPi.GPIO as GPIO
import time
import picamera
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
trig = 6 ; echo = 5 #센서에 연결한 Trig와 Echo 핀의 핀 번호 설정
print ("start")

GPIO.setup(trig, GPIO.OUT); GPIO.setup(echo, GPIO.IN)  #Trig와 Echo 핀의 출력/입력 설정
GPIO.output(trig, False) #Trig핀의 신호를 0으로 출력
print("Waiting for sensor to settle")


password = [1,3,4,2,1,4]
password_match = []
match_error=[]
p = GPIO.PWM(18, 100) 

def send_an_email():
	with picamera.PiCamera() as camera:
			camera.resolution = (640, 480)
			camera.start_preview()
			time.sleep(1)
			camera.capture('invader.jpg')
			camera.stop_preview()
	toaddr = "bomin2641@gmail.com"
	me = "bomin2641@gmail.com"
	subject = "WARNING!!!!! INVADER"
				
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = toaddr
	msg.preamble = "test"
				
	part = MIMEBase('application',"octet-stream")
	part.set_payload(open("invader.jpg", "rb").read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="invader.jpg"')
	msg.attach(part)
				
	try:
		s = smtplib.SMTP('smtp.gmail.com',587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(user = 'bomin2641@gmail.com', password = 'kimbomin2')
		s.sendmail(me,toaddr,msg.as_string())
		s.quit()
	except SMTPException as error:
		print("Eroor")
					
def button_callback(channel):
	global light_on
	if channel == button_pin1:
		password_match.append(1)
		GPIO.output(led_pin1,1)
		time.sleep(0.1)
		GPIO.output(led_pin1,0)
		print("LED1 ON!")
		light_on = not light_on
	elif channel == button_pin2:
		password_match.append(2)
		GPIO.output(led_pin2,1)
		time.sleep(0.1)
		GPIO.output(led_pin2,0)
		print("LED2 ON!")
		light_on = not light_on	
	elif channel == button_pin3:
		password_match.append(3)
		GPIO.output(led_pin3,1)
		time.sleep(0.1)
		GPIO.output(led_pin3,0)
		print("LED3 ON!")
		light_on = not light_on	
	elif channel == button_pin4:
		password_match.append(4)
		GPIO.output(led_pin4,1)
		time.sleep(0.1)
		GPIO.output(led_pin4,0)
		print("LED4 ON!")
		light_on = not light_on		
	print(password)
	print(password_match)
	if len(password_match) == 6 :
		if password==password_match :
			print("ok")
			p.start(10)
			p.ChangeFrequency(262)
			GPIO.output(led_pin1,1)
			time.sleep(0.3)
			GPIO.output(led_pin1,0)
			p.ChangeFrequency(330)
			GPIO.output(led_pin2,1)
			time.sleep(0.3)
			GPIO.output(led_pin2,0)
			p.ChangeFrequency(392)
			GPIO.output(led_pin3,1)
			time.sleep(0.3)
			GPIO.output(led_pin3,0)
			p.ChangeFrequency(540)
			GPIO.output(led_pin4,1)
			time.sleep(0.3)
			GPIO.output(led_pin4,0)
			password_match.clear()
			p.stop()	
		else :
			match_error.append(1)
			print("nope")
			print(match_error)
			p.start(10)
			p.ChangeFrequency(350)
			GPIO.output(led_pin1,1)
			time.sleep(0.1)
			GPIO.output(led_pin1,0)
			time.sleep(0.1)
			GPIO.output(led_pin1,1)
			time.sleep(0.1)
			GPIO.output(led_pin1,0)
			time.sleep(0.1)
			GPIO.output(led_pin1,1)
			time.sleep(0.1)
			GPIO.output(led_pin1,0)
			time.sleep(0.1)		
			GPIO.output(led_pin1,1)
			time.sleep(0.1)
			GPIO.output(led_pin1,0)
			time.sleep(0.1)			
			GPIO.output(led_pin1,1)
			time.sleep(0.1)
			GPIO.output(led_pin1,0)
			p.stop()	
			password_match.clear()	
			if len(match_error) == 3:
				p.start(10)
				p.ChangeFrequency(262)
				GPIO.output(led_pin1,1)
				time.sleep(0.3)
				GPIO.output(led_pin1,0)
				p.ChangeFrequency(330)
				GPIO.output(led_pin1,1)
				time.sleep(0.3)
				GPIO.output(led_pin1,0)
				p.ChangeFrequency(262)
				GPIO.output(led_pin1,1)
				time.sleep(0.3)
				GPIO.output(led_pin1,0)
				p.ChangeFrequency(330)
				GPIO.output(led_pin1,1)
				time.sleep(0.3)
				GPIO.output(led_pin1,0)
				password_match.clear()
				p.stop()	
				print("send email!!!!")
				send_an_email()	
			
			
	
		
		
button_pin1 = 15
led_pin1 = 4

button_pin2 = 23
led_pin2 = 17

button_pin3 = 24
led_pin3 = 27

button_pin4 = 25
led_pin4 = 22

GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM)


GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(led_pin1,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
GPIO.setup(led_pin3,GPIO.OUT)
GPIO.setup(led_pin4,GPIO.OUT)

light_on = False
GPIO.add_event_detect(button_pin1,GPIO.RISING,callback=button_callback,bouncetime=500)
GPIO.add_event_detect(button_pin2,GPIO.RISING,callback=button_callback,bouncetime=500)
GPIO.add_event_detect(button_pin3,GPIO.RISING,callback=button_callback,bouncetime=500)
GPIO.add_event_detect(button_pin4,GPIO.RISING,callback=button_callback,bouncetime=500)
print("check")
t=0
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
		if distance<50:
			t+=1
			print(t)
			if t>15:
				p.start(10) 
				p.ChangeFrequency(262)
				time.sleep(0.3)
				p.stop()
				send_an_email()
		else :
			t=0
			print(t)
		time.sleep(1)	

while 1:
	time.sleep(0.1)




