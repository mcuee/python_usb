#!/usr/bin/env python

import usb.core
import usb.util


if __name__=="__main__":
#find our device
        dev = usb.core.find(idVendor=0x04D8, idProduct=0x0033)

#was it found?
        if dev is None:
                raise ValueError('Device not found')

#set the active configuration. with no args we use first config.
        dev.set_configuration()

        packet_len=64
        # To get firmware version number
        print ("Sending version command by USB interrupt write")
        dev.write(0x01,"v"+(packet_len-1)*"Z",1000)
        print ("Getting version command by USB interrupt read")
        r=dev.read(0x81,packet_len,1000)
        print ("Firware version is", r[0],".",r[1])