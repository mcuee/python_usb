#!/usr/bin/env python

import usb.core
import usb.util

#find our device
dev = usb.core.find(idVendor=0x04D8, idProduct=0x0053)
#dev = usb.core.find(idVendor=0x04D8, idProduct=0x0033)

#was it found?
if dev is None:
   raise ValueError('Device not found')

#set the active configuration. with no args we use first config.
dev.set_configuration()

#turn light on
print ("Toggle LED by sending Toggle_LED command 0x80")
dev.write(1, [0x080], 1000)

print ("Sending read switch command")
dev.write(1,[0x081],1000)
s=dev.read(0x81,64,1000)
print ("Echo read switch command 0x81")
print (s[0])
print ("Read switch status, 1 means not pressed, 0 means pressed")
print (s[1])
#dev.reset()
