#!/usr/bin/python

### quick mod from https://github.com/danielkucera/cyusb3014-breakout/blob/master/software/loopback-test.py

import usb.core
import usb.util
import time
import _thread

# find our device
dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f1 )

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

dev.set_interface_altsetting(interface = 0, alternate_setting = 1)
intf = cfg[(0,1)]

#print intf

ep = usb.util.find_descriptor(
    intf,
    # match the OUT endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x03)

ep2 = usb.util.find_descriptor(
    intf,
    # match the IN endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x83)

assert ep is not None
assert ep2 is not None

print ('ep:',ep)
print ('ep2:',ep2)

chunkr = 2**16
chunkw = 2**16

print ("Starting CYUSB3014 python isoc sourcesink test")

def read_loop():
    start = time.time()
    trans = 0
    while True:
        data = dev.read(0x81, chunkr, 1000)
        trans = trans + len(data)
        if time.time() > start + 1:
            bps = trans/(time.time() - start)
            print ("Read: transfered %d kB/s" % (bps/(1024)) )
            trans = 0
            start = time.time()

def write_loop():
    start1 = time.time()
    trans1 = 0
    dat = "A"*chunkw
    while True:
        ep.write(dat)
        trans1 = trans1 + len(dat)
        if time.time() > start1 + 1:
            bps1 = trans1/(time.time() - start1)
            print ("Write: transfered %d kB/s" % (bps1/(1024)) )
            trans1 = 0
            start1 = time.time()

_thread.start_new_thread( write_loop, () )

read_loop()

