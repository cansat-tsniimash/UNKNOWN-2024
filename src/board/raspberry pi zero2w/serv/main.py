import RPI.GPIO as GPIO


def setAngle(serv, ang):
    duty = ang / 18 + 2
    serv.ChangeDutyCircle(duty)



GPIO.setmode(GPIO.BMC)
GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18, 50)
servo.start(0)

GPIO.output(servo, True)

angle = 73


setAngle(servo, angle)