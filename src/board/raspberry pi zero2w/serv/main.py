import RPi.GPIO as GPIO
import time

def setAngle(serv, ang):
    duty = ang / 18 + 2
    serv.ChangeDutyCycle(duty)



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 50)
servo.start(0)
print(servo)


angle = 180
setAngle(servo, angle)
time.sleep(10)
servo.stop()
GPIO.cleanup()


#setAngle(servo, angle)