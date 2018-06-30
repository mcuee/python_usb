#!/usr/bin/env python

import usb.core
import usb.util

#find our device
dev = usb.core.find(idVendor=0x04D8, idProduct=0x003f)

#was it found?
if dev is None:
   raise ValueError('Device not found')

#for configuration in dev:
#   for interface in configuration:
#       ifnum = interface.bInterfaceNumber
#       if not dev.is_kernel_driver_active(ifnum):
#           continue
#       try:
#           print ("detach kernel driver from device %s: interface %s" % (dev, ifnum))
#           dev.detach_kernel_driver(ifnum)
#      except usb.core.USBError, e:
#           pass

#set the active configuration. with no args we use first config.
dev.set_configuration()

#turn light on
print ("Toggle LED by sending Toggle_LED command")
dev.write(1, [0,0x080], 1000)

print ("Sending read switch command")
dev.write(1,[0,0x081],1000)
s=dev.read(0x81,64,5000)
print ("Echo read switch command 0x81")
print (s[0])
print ("Read switch status, 1 means not pressed, 0 means pressed")
print (s[1])
#dev.reset()
