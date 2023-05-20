#!/usr/bin/python

### quick mod from https://github.com/danielkucera/cyusb3014-breakout/blob/master/software/loopback-test.py

import usb.core
import usb.util
import time
import _thread

# find our device
dev = usb.core.find(idVendor=0x04b4, idProduct=0x1003)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

dev.set_interface_altsetting(interface = 0, alternate_setting = 6)
intf = cfg[(0,6)]

print(intf)

ep2 = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x6)


assert ep2 is not None

#print ('ep2:',ep2)

chunkr = 2**16

print ("Starting CYUSB FX2LP python isoc read test")

def read_loop():
    start = time.time()
    trans = 0
    while True:
        data = dev.read(0x82, chunkr, 1000)
        trans = trans + len(data)
        if time.time() > start + 1:
            bps = trans/(time.time() - start)
            print ("Transfered %d kB/s" % (bps/(1024)) )
            trans = 0
            start = time.time()


read_loop()

