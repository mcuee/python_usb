#!/usr/bin/env python

import usb.core
import usb.util
from usb.backend import libusb1
be = libusb1.get_usbdk_backend()

dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f0, backend = be)

if dev is None:
    raise ValueError('Device not found')

print("Device found")

dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

intf = cfg[(0,0)]

print(intf)


ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 1)

ep2 = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        e.bEndpointAddress == 0x81)

assert ep is not None
assert ep2 is not None

print ('ep:',ep)
print ('ep2:',ep2)