#!/usr/bin/env python
# quick mod from https://github.com/trezor/cython-hidapi/blob/master/try.py
# for the generic hid fw here: http://janaxelson.com/hidpage.htm

from __future__ import print_function

import hid
import time

# enumerate USB devices

for d in hid.enumerate():
    keys = list(d.keys())
    keys.sort()
    for key in keys:
        print("%s : %s" % (key, d[key]))
    print()

# try opening a device, then perform write and read

try:
    print("Opening the device")

    h = hid.device()
    h.open(0x0925, 0x7001)  # Lakeview Research Generic HID VendorID/ProductID

    print("Manufacturer: %s" % h.get_manufacturer_string())
    print("Product: %s" % h.get_product_string())
    #print("Serial No: %s" % h.get_serial_number_string())

    # enable non-blocking mode
    h.set_nonblocking(1)

    # write some data to the device
    print("Write the data")
    h.write([0, 0x41, 0x42] + [0] * 62)

    # wait
    time.sleep(0.05)

    # read back the answer
    print("Read the data")
    while True:
        d = h.read(64)
        if d:
            print(d)
        else:
            break

    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard-coded device.")
    print("Update the h.open() line in this script with the one")
    print("from the enumeration list output above and try again.")

print("Done")
