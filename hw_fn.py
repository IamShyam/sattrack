import time
import RPi.GPIO as GPIO
from magnetometer_interface import Magnetometer
from motor_interface import DCmotor
from servo_interface import ServoMotor

GPIO.setmode(GPIO.BCM)

def initialize_hardware():
    return ServoMotor(22, 100), DCmotor(18, 17), Magnetometer()


#s, d, m = initialize_hardware()
#GPIO.cleanup()
