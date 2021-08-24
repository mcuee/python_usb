#!/usr/bin/env python
# https://github.com/pyusb/pyusb/issues/384

import time
import usb.core
import usb.util
import usb.backend.libusb1

be = usb.backend.libusb1.get_backend()

# find our device Arduino Leonardo idVendor=0x2341, idProduct=0x8036
dev = usb.core.find(idVendor=0x2341, idProduct=0x8036, backend=be)

if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
#print(cfg)
intf0 = cfg[(0,0)]
print(intf0)
intf1 = cfg[(1,0)]
print(intf1)

epout = usb.util.find_descriptor(
    intf1,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)
      

assert epout is not None

# write the data
print("Turning the LED ON")
epout.write('2')
time.sleep(1)
print("Turning the LED OFF")
epout.write('1')

