#!/usr/bin/env python
# https://github.com/rene-aguirre/pywinusb/issues/56

import pywinusb.hid

class C:
  def __init__(self,h):
    self.h = h
  def __del__(self):
    print("closing")
    self.h.close()
    print("closed")

h = pywinusb.hid.HidDeviceFilter().get_devices()[0]
h.open()
c = C(h)

# del c  # this is needed for Python 3.6/3.7/3.8 (if not Python will hang) but not needed for Python 3.9 based on testing
