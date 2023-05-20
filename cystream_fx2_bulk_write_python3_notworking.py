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

dev.set_interface_altsetting(interface = 0, alternate_setting = 2)
intf = cfg[(0,2)]

print(intf)

ep = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x06)

assert ep is not None

#print ('ep:',ep)

chunkw = 2**16

print ("Starting CYUSB FX2LP SyStream python bulk write test")

def write_loop():
    dat = "A"*chunkw
    while True:
        try:
            ep.write(dat)
        except:
            pass

write_loop()