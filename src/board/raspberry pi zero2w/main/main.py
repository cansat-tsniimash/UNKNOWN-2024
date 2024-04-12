import socket
import time
import select
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time

def setAngle(serv, ang):
    duty = ang / 18 + 2
    serv.ChangeDutyCycle(duty)


picam2 = Picamera2()

addr = '98:DA:60:0A:0E:C3'


poller = select.epoll()
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((addr, 1))


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 50)


poller.register(sock.fileno(), select.EPOLLIN | select.EPOLLERR)

while True:
	poll_rc = poller.poll()
	if not poll_rc:
		continue
	
	data = sock.recv(4096)
	#print(data)
	if(data[6] == 0):
		word = data[2:6].decode("ascii")
	else:
		word = data[2:7].decode("ascii")
	#print(word)
		if word == "start":
		picam2.start_and_record_video(output="/home/knpn/main/main_video.mp4", duration=0)
		servo.start(0)
		#print('i started')
	if word == "stop":
		picam2.stop_recording()
		servo.stop()
		GPIO.cleanup()
	if word == "angle":
		angle = data[7:12].decode("ascii")
		setAngle(servo, angle)





