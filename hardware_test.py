from hardware import Hardware
from time import sleep

hardware = Hardware()
hardware.connect()
hardware.set_target(0, 0)
angle = 0
f = 1
try:
    while True:
        angle += f*1
        if angle == 180 or angle == 0: f = -1* f
        #angle %= 180
        hardware.set_target(0, (angle-90))
        hardware.loop()
        sleep(0.01)
except KeyboardInterrupt:
    hardware.stop()

