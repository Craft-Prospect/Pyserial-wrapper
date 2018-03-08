#!/usr/bin/env python

"""host.py: Host script for serial read/write"""

__author__ = "Murray Ireland"
__email__ = "murray.ireland@craftprospect.com"
__date__ = "07/03/2018"
__copyright__ = "Copyright 2018 Craft Prospect Ltd"

import time
from serial_wrapper import Serial

# Create serial object
ser = Serial("/dev/ttyUSB1")

# Check it's open
if ser.is_open():
    print("Serial port is open")

# Run client script
ser.write_terminal_cmd("python3.6 ~/python/Pyserial-wrapper/client.py")

# time.sleep(0.1)

def read_data(ZERO_TIME):
    # Read data transmission
    data = {"time": [], "signal": []}
    loop = True
    while loop == True and time.time() - ZERO_TIME <= 10:
        rcvd = ser.readline(timeout=0.02)
        if rcvd != None:
            print(rcvd)
            if "end_connection" in rcvd:
                loop = False
            else:
                datapoint = rcvd.split(",")
                data["time"].append(float(datapoint[0]))
                data["signal"].append(float(datapoint[1]))

    return data

handshake, zero_time = ser.send_handshake()

DELAY = 0.5
time.sleep(DELAY)

if handshake:
    print("Zero time: {:.2f}s".format(zero_time))
    data = read_data(zero_time + DELAY)
    # print(data)

# Close serial port
print("Closing port")
ser.close()

# Display data
if handshake:
    import matplotlib.pyplot as plt

    plt.plot(data["time"], data["signal"])
    plt.show()
