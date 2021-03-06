import threading
import time
import hw_fn
from magnetometer_interface import *
from motor_interface import *
from servo_interface import *

#import serial

from PID import PID

s,d,m = hw_fn.initialize_hardware()


class Hardware:
    def __init__(self):
        self.pid = PID(2, 0.10, 20)  # 3 0.8 20 # Trial and Error values
        self.pid.setWindup(75)  # 100
        self.top_arduino = None
        self.base_arduino = None

        self.base_target = None  # Current target for PID

        self.thread = None
        self.looping = False  # If thread is running
        self.thread_shutdown = False

    def connect(self, port1="COM4", port2="COM6"):
       # initialize_hardware()        
        print " NO connection required"
        #        print "Initializing Bluetooth Connection..."
#        self.top_arduino = serial.Serial(port1, 9600, timeout=1)  # open serial port that Arduino is using
#        print "Connecting to Arduino..."
#        self.base_arduino = serial.Serial(port2, 9600, timeout=1)  # open serial port that Arduino is using
#        self.top_arduino.flushInput()
#        self.top_arduino.read(10000)  # clear buffer because Arduino has been sending values

    def set_motor(self, val):
        """write to base arduino"""

        val = int(val)
        val2 = min(abs(val), 99)
        
#        if self.print "Val: "+str(val)+" "+str(val2)
        if val >= 0: d.motor_move_counter_clockwise(val2)  # value range of arduino analogWrite()
        if val < 0: d.motor_move_clockwise(val2)
#        self.base_arduino.write(str(val) + '\n')


    def read_mag(self):
        try:
            return get_azimuth(m)
        except:
            return None

    def set_servo(self, angle):
        """Convert angle for servo to the required PWM signal range"""
        #angle = angle + 90
        
        
        if angle > 90: angle = 90
        if angle < -90: angle = -90
        angle += 90  # 0 - 180 range
        s.update_servo_position(angle)
#        angle = 180 - angle  # invert because of placement of servo
#
#        val = float(angle) / 180 * 1800 + 550  # convert to range as found by testing
#        val = str(int(val)) + '!'  # endline convention as adopted; also followed in Arduino
#        # padding 0 as convention adopted
#        while len(val) < 5:
#            val = '0' + val
#
 #       self.top_arduino.write(val)

    def convert_mag(self, mag):
#        """Covert angle measured by magnetometer to azimuth convention (Clockwise from North)"""
#        if mag != 0: mag = 360 - mag  # counter clockwise to clockwise
#        mag = mag - 26 + 30 + 20 - 5  # fixed error of magnetometer
#        if mag < 0: mag = 360 + mag  # warp around
        return mag

    def stop_thread(self):
        if not self.looping: return  # Can't shut down thread if it's not runnning
        print "Stopping Thread..."
        self.looping = False  # Shut down Thread
        while not self.thread_shutdown:  # wait for thread shut down
            pass
        d.stop_transmission()
        s.terminate_servo()
        self.thread_shutdown = False  # reset variable for next use

        print "Successfully shut down thread..."
        exit()

    def stop(self):
        print
        self.stop_thread()
       #self.top_arduino.close()
        #self.base_arduino.close()
        self.set_motor(0)
        s.terminate_servo()
        d.stop_transmission()

        self.pid.clear()

    def find_error(self):
        """
        Find the error between target and current base position
        :return:
        """
        mag = self.read_mag()
        if mag is None: return None
        mag = self.convert_mag(mag)
        error = self.base_target - mag
        if error < 0: error = 360 + error  # convert to 0 - 360 from -x to -x + 360
        if error > 180: error = -(360 - error)  # convert to -180 to 180
        return error

    def set_target(self, azimuth, elevation):
        self.set_servo(elevation)
        self.base_target = azimuth

    def loop(self):
        """
        Loop so that the PID controller can run and adjust base to the target
        """
#        if self.base_target is None: return None
        error = self.find_error()
        if error is None: return
        self.pid.update(error)
        self.set_motor(self.pid.output)
 #       print "error: "+str(error)
        return error

    def run_loop(self, period=0.01, verbose=False):
        """
        :param period: time period of loop
        """

        print "Starting Thread..."

        def to_run():
            while True:
                if not self.looping: break  # stop thread
                e = self.loop()
#                if verbose: print e
                time.sleep(period)
            self.thread_shutdown = True

        self.looping = True  # keep track of thread state
        self.thread = threading.Thread(target=to_run)
        self.thread.setDaemon(False)  # don't keep thread running in the back ground
        self.thread.start()
        print "Thread Started..."
