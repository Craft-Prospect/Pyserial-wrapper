#!/usr/bin/env python

"""client_blank.py: Client script for serial read/write"""

import time
from serial_wrapper import Serial

# Start client timer
TIME_INIT = time.time()

# Create serial port object
ser = Serial("/dev/ttyPS0")

zero_time = ser.listen_for_handshake()

# Close serial port  
ser.close()
