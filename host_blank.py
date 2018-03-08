#!/usr/bin/env python

"""host_blank.py: Host script for serial read/write"""

import time
from serial_wrapper import Serial

# Create serial object
ser = Serial("/dev/ttyUSB1")

# Check it's open
if ser.is_open():
    print("Serial port is open")

# Run client script
cmd = "python3.6 ~/python/Pyserial-wrapper/client_blank.py"
print("Sending command: {}".format(cmd))
ser.write_terminal_cmd(cmd)

handshake, zero_time = ser.send_handshake()

# Close serial port
print("Closing port")
ser.close()
