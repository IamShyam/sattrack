import time
from motor_interface import DCmotor
from magnetometer_interface import *
import math


dcm = DCmotor(18, 17)
mag = Magnetometer()

ra = 180 


def correct_azimuth():
    while True:
        ha = get_azimuth(mag)
        print "ha: " + str(ha)
        if 360-(ha-ra) <= 5 or abs(ha-ra) <= 5:
            break
        #elif (((ha - ra) <= 180) and ((ha - ra) > 0)) or ((ha - ra) <= -180):
        elif (180 + ra) > ha:
            err = 360 - (ha-ra)
            print "cc error: "+str(err)
            b = -0.766
            x =(-b + math.sqrt(b**2 + 0.072*err))/0.036
            dcm.motor_move_clockwise(int(x))
                
        #elif (((ha - ra) < 0) and ((ha - ra) > -180)) or ((ha - ra) > 180):
        elif (180 + ra) < ha:
            err = abs(ra-ha)
            print "c error: "+str(err)
            b = -0.766
            x =(-b + math.sqrt(b**2 + 0.072*err))/0.036
            dcm.motor_move_counter_clockwise(int(x))
    print "hurrahe"
    
correct_azimuth()
