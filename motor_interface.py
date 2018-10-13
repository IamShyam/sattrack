import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class DCmotor():
    def __init__(self, in1, in2):
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        self.p = GPIO.PWM(in1, 100)
        self.q = GPIO.PWM(in2, 100)
        #a = 1
        #print a
        self.p.start(0)
        self.q.start(0)
        print "DC Motor Initialised"

    def motor_move_clockwise(self, reps=150):

        self.p.ChangeDutyCycle(reps)
        self.q.ChangeDutyCycle(0)
        '''        lim = reps/2
        for i in range(lim):
            self.p.ChangeDutyCycle(i)
            #print "hi1"
            time.sleep(0.02)
        for i in range(lim):
            self.p.ChangeDutyCycle(lim-i)
	    #print "hi2"
            time.sleep(0.02)
        #print a+1'''

    def motor_move_counter_clockwise(self, reps=150):
        self.q.ChangeDutyCycle(reps)
        self.p.ChangeDutyCycle(0)
        '''        lim = reps/2
        for i in range(lim):
            self.q.ChangeDutyCycle(i)
	    #print "he1"
            time.sleep(0.02)
        for i in range(lim):
            self.q.ChangeDutyCycle(lim-i)
	    #print "he2"
            time.sleep(0.02)'''

    def stop_transmission(self):
        self.p.stop()
        self.q.stop()

'''motor = DCmotor(17,18)

try:
    while True:
        motor.motor_move_clockwise(102)
        time.sleep(0.5)
        motor.motor_move_counter_clockwise(100)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

motor.stop_trasmission()
print "Transmission Completed"
GPIO.cleanup()'''
