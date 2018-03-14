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
ser.write_terminal_cmd("python3.6 ~/python/zynq-tests/client.py")

# time.sleep(0.1)

# Send handshake and check for receipt
def send_handshake():
    ZERO_TIME = None
    handshake = False

    t0 = time.time()
    while handshake == False and time.time() - t0 < 5:
        # Send handshake
        ser.send_handshake()

        # Listen for stuff
        rcvd = ser.readline(timeout=0.01)
        if rcvd != None and "received" in rcvd:
            ZERO_TIME = time.time()
            handshake = True

    if handshake:
        print("Handshake received")
        print("Client and host connected")
    else:
        print("Handshake not received, timed out")

    return handshake, ZERO_TIME

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

handshake, zero_time = send_handshake()

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
