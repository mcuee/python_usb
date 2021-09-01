# codes from https://github.com/vpelletier/python-libusb1/issues/72

import usb1

class USB:
    """USB class that handles IO operation with USB device
    ENDPOINT_IN: device-to-host, ENDPOINT_OUT: host-to-device"""
    # read size chunk
    READ_CHUNK = 1024

    def __init__(self, pid: hex, vid: hex, endpoint_in: hex, endpoint_out: hex) -> None:
        self.endpoint_in = endpoint_in
        self.endpoint_out = endpoint_out
        self.pid = pid
        self.vid = vid
        self.context = usb1.USBContext()

    def is_connected(self) -> bool:
        """Check if specified device is connected"""
        with usb1.USBContext() as context:
            for device in context.getDeviceIterator(skip_on_error=True):
                if device.getVendorID() == self.vid and device.getProductID() == self.pid:
                    return True

    def open(self) -> bool:
        """Open USB and initialize interface"""
        try:
            self.context.open()
            return True
        except Exception as err:
            print("open device error:", err)
            return False

    def __get_handle(self):
        """return handle object"""
        return self.context.openByVendorIDAndProductID(self.vid, self.pid)

    def close(self) -> bool:
        """Close USB"""
        print("Closing USB")
        try:
            self.context.close()
            print("Close handle successfully")
            return True
        except Exception as err:
            print("Close handle error:", err)
            return False

    def write_read(self, msg: bytearray, timeout: int = 0) -> bytearray:
        """write an specific msg to device and then read"""
        data = bytearray()
        handle = self.__get_handle()
        with handle.claimInterface(0):
            handle.bulkWrite(self.endpoint_out, msg, timeout)
            bytes_written = len(msg)
            print("Number of bytes written: ", bytes_written)
            data += handle.bulkRead(self.endpoint_in,
                                        self.READ_CHUNK, timeout)
        handle.close()    
        return data

    def __del__(self):
        print("Calling closing method to delete self")
        self.close()


if __name__ == '__main__':
    VENDOR_ID = 0x04b4
    PRODUCT_ID = 0x00f0
    ENDPOINT_IN = 0x81
    ENDPOINT_OUT = 0x01
    usb = USB(PRODUCT_ID, VENDOR_ID, ENDPOINT_IN, ENDPOINT_OUT)
    #print(usb.is_connected())
    msg = 100 * bytearray(b"B")
    if usb.open():
        print("Reading back:", usb.write_read(msg))
    # no error after adding this line
    usb.close()
