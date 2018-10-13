import time
import math
import smbus

bus = smbus.SMBus(1)
channel = 0x1e
pi = math.pi

class Magnetometer():
    def __init__(self):
        bus.write_byte_data(channel, 0x00, 0x70)
        bus.write_byte_data(channel, 0x01, 0xA0)
        bus.write_byte_data(channel, 0x02, 0x00)

    def read_data(self, addr):
        msb = bus.read_byte_data(channel, addr)
        lsb = bus.read_byte_data(channel, addr+1)
        data = (msb<<8) | lsb

        if data > 32768:
            data = data - 65536

        return data

def get_azimuth(m):
    x = m.read_data(0x03)
    z = m.read_data(0x05)
    y = m.read_data(0x07)
    heading_angle = math.atan2(-x,-z)
    if heading_angle > 2*math.pi:
        heading_angle = 2*math.pi - heading_angle
    elif heading_angle < 0:
        heading_angle = 2*math.pi + heading_angle

#    print heading_angle*180/math.pi
    return heading_angle*180/math.pi



'''
meter = Magnetometer()
try:
    while True:
        get_azimuth(meter)
except KeyboardInterrupt:
    pass
try:
    while True:
        x_val = meter.read_data(0x03)
        z_val = meter.read_data(0x05)
        y_val = meter.read_data(0x07)

	heading_angle = math.atan2(-x_val,-z_val)

	if heading_angle > 2*math.pi:
	    heading_angle = 2*math.pi - heading_angle

	elif heading_angle < 0:
	    heading_angle = 2*math.pi + heading_angle

#        print str(x_val)+", "+str(y_val)+", "+str(z_val)
	print (heading_angle *180/(math.pi))
	time.sleep(0.01)

except KeyboardInterrupt:
    pass'''
