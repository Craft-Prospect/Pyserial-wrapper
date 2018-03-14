#!/usr/bin/env python

"""serial_wrapper.py: Useful functions for serial scripts"""

__author__ = "Murray Ireland"
__email__ = "murray.ireland@craftprospect.com"
__date__ = "23/02/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import serial, time

class Serial(object):
    """Class for wrapper around serial class"""

    HANDSHAKE = "Pynq panther"

    def __init__(self, port, baudrate=115200, timeout=0.001):
        """Instantiate object"""

        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def write(self, send):
        """Custom write function"""

        self.ser.write(send.encode("ascii"))

    def read(self, num_bytes=1):
        """Custom read function"""

        rcvd = self.ser.read(num_bytes)
        
        return rcvd.decode("ascii")

    def writeline(self, send):
        """Custom write line function"""

        self.ser.write((send + "\r").encode("ascii"))

    def write_terminal_cmd(self, send):
        """Write command to client terminal"""

        self.ser.write((send + "\n").encode("ascii"))

    def readline(self, timeout=None):
        """Custom readline function, since built-in one is really bad"""

        rcvd = b""
        t0 = time.time()
        while time.time() - t0 < timeout or timeout == None:
            chr = self.ser.read()
            if chr == b"\r":
                return rcvd.decode("ascii")
            rcvd += chr

        if rcvd == b"" and timeout != None:
            return None

    def is_open(self):
        """Check serial port is open"""

        return self.ser.is_open

    def close(self):
        """Close serial port"""

        self.ser.close()

    def send_handshake(self):
        """Send handshake phrase to client"""

        self.writeline(self.HANDSHAKE)