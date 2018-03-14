#!/usr/bin/env python

"""client.py: Client script for serial read/write"""

__author__ = "Murray Ireland"
__email__ = "murray.ireland@craftprospect.com"
__date__ = "07/03/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import time
from serial_wrapper import Serial
from numpy import sin, cos

# Start client timer
TIME_INIT = time.time()

# Create serial port object
ser = Serial("/dev/ttyPS0")

# Wait for handshake
def listen_for_handshake():
    ZERO_TIME = None
    handshake = False
    loop = True
    t0 = time.time()
    while handshake == False and time.time() - t0 < 5:
        rcvd = ser.readline(timeout=0.01)
        if rcvd == ser.HANDSHAKE:
            for i in range(0, 1):
                ser.writeline("received")
            ZERO_TIME = time.time()
            handshake = True

    return ZERO_TIME

# Data transmission
def write_data(ZERO_TIME):
    client_time = 0
    while client_time <= 5:
        client_time = time.time() - ZERO_TIME

        # Periodic wave for testing
        signal = sin(4*client_time)*cos(8*client_time)

        # Write data
        send = "{:.5f},{:.5f}".format(client_time, signal)
        ser.writeline(send)
        time.sleep(0.01)

zero_time = ser.listen_for_handshake()

DELAY = 0.5
time.sleep(DELAY)

write_data(zero_time + DELAY)

ser.writeline("end_connection")

# Close serial port  
ser.close()
