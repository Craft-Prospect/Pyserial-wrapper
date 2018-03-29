#!/usr/bin/env python

"""serial_wrapper.py: Useful functions for serial scripts"""

__author__ = "Murray Ireland"
__email__ = "murray.ireland@craftprospect.com"
__date__ = "23/02/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import serial, time
# from tqdm import tqdm
import numpy as np

class Serial(object):
    """Class for wrapper around serial class"""

    HANDSHAKE = "Pynq panther"

    def __init__(self, port, baudrate=115200, timeout=0):
        """Instantiate object"""

        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def write_raw(self, send):
        """Raw write function"""

        self.ser.write(send)

    def read_raw(self, num_bytes=1):
        """Raw read function"""

        return self.ser.read(num_bytes)

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

    def in_waiting(self):
        """Check bytes in waiting"""

        return self.ser.in_waiting

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

    def send_ready(self):
        """Send ready signal for following data"""

        self.writeline("ready")

    def get_ready(self, pause=0.5, wait_time=5, verbose=False):
        """Listen for ready signal for following data"""

        t0 = time.time()
        loop = True
        while loop and time.time() - t0 < wait_time:
            time.sleep(0.5)
            if verbose: print("Waiting for ready signal")
            rcvd = self.readline(timeout=0.02)
            if rcvd != None and "ready" in rcvd:
                loop = False

        if verbose and time.time() - t0 < wait_time:
            print("Data ready to receive")

    def read_data(self, max_bytes=float("inf"), max_time=float("inf"), max_blanks=float("inf"), verbose=False):
        """Read data in form of byte array"""

        if max_bytes == float("inf") and max_time == float("inf") and max_blanks == float("inf"):
            max_time = 10

        rcvd_acc = bytearray()
        total_bytes = 0
        running_blanks = 0
        t0 = time.time()
        t = 0
        while total_bytes < max_bytes and t < max_time and running_blanks < max_blanks:
            num_bytes = self.in_waiting()
            rcvd = self.ser.read(num_bytes)
            rcvd_acc.extend(rcvd)
            total_bytes += num_bytes
            if num_bytes == 0:
                running_blanks += 1
            else:
                running_blanks = 0
            if running_blanks > 100:
                t0 = time.time()
            if verbose and num_bytes > 0:
                print("Time: {:.2f}s, bytes: {}".format(t, num_bytes))
                # print(rcvd[:20])
            time.sleep(0.01)
            t = time.time() - t0

        rcvd_acc = list(rcvd_acc)

        return rcvd_acc
