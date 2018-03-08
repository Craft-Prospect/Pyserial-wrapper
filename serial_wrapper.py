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

    def __init__(self, port, baudrate=115200, timeout=0):
        """Instantiate object"""

        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def write(self, send):
        """Custom write function"""

        self.ser.write(send.encode("ascii"))

    def read(self):
        """Custom read function"""

        rcvd = self.ser.read(self.ser.in_waiting)
        
        return str(rcvd.decode("ascii"))

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

    def flush(self):
        """Flush serial port"""

        self.ser.flush()

    def close(self):
        """Close serial port"""

        self.ser.close()

    def send_handshake(self, wait_time=5):
        """Send handshake phrase to client"""

        print("Sending handshake")

        ZERO_TIME = None
        handshake = False

        t0 = time.time()
        while handshake == False and time.time() - t0 < wait_time:
            # Send handshake
            self.writeline(self.HANDSHAKE)

            # Listen for stuff
            rcvd = self.readline(timeout=0.01)
            if rcvd != None and "received" in rcvd:
                ZERO_TIME = time.time()
                handshake = True

        if handshake:
            print("Handshake received")
            print("Client and host connected")
        else:
            print("Handshake not received, timed out")

        return handshake, ZERO_TIME

    def listen_for_handshake(self, wait_time=5):
        """Listen for handshake from host"""

        ZERO_TIME = None
        handshake = False

        t0 = time.time()
        while handshake == False and time.time() - t0 < wait_time:
            rcvd = self.readline(timeout=0.01)
            if rcvd == None:
                rcvd = ""
            if rcvd != None and self.HANDSHAKE in rcvd:
                for i in range(0, 1):
                    self.writeline("***received***")
                ZERO_TIME = time.time()
                handshake = True

        return ZERO_TIME