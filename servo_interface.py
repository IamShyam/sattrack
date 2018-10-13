import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class ServoMotor():
    def __init__(self,channel, frequency):
        GPIO.setup(channel, GPIO.OUT)
        self.pwm = GPIO.PWM(channel, frequency)
        self.pwm.start(5)
        print "Servo Initialised"

    def update_servo_position(self, angle):
#        if angle >= 90:
#            dutycycle = 21 - (float(angle)*16)/180
        dutycycle = 21 - (float(180 - angle)*16)/180
#        elif angle >= 45 and angle < 90:
#            dutycycle =  18- (float(angle)*5)/90
#	elif angle<45:
#	    dutycycle = 22 - (float(angle)*4)/45

        self.pwm.ChangeDutyCycle(dutycycle)
	#self.pwm.stop()

    def terminate_servo(self):
        self.pwm.stop()
        #GPIO.cleanup()

'''servo = ServoMotor(22, 100)

try:
    while True:
        x = raw_input("Enter an angle: ")
        servo.update_servo_position(x)
except KeyboardInterrupt:
    servo.terminate_servo()
    pass

GPIO.cleanup()'''
