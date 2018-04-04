#!/usr/bin/env python

"""host_bytearray.py: Host script for serial read/write"""

import time, cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from serial_wrapper import Serial

# Pre-append time to log entry
def write_time(text):
    now = time.localtime(time.time())
    text = "{:02d}:{:02d}:{:02d} - {:s}".format(now[3], now[4], now[5], text)

    return text

# Header text
now = time.localtime(time.time())
print("File: host_bytearray.py")
print(time.asctime(now))
print("")

# Create serial object
print(write_time("Connecting to serial port"))
ser = Serial("/dev/ttyUSB1")
ser.flush()

# time.sleep(2)

print(write_time("Starting client"))
ser.write_terminal_cmd("python3.6 ~/python/Pyserial-wrapper/client_bytearray.py")

# Check script is running
check = ser.readline(5)

# Send handshake
send_data = False
if check != None and "running" in check:
    print(write_time("Running client script detected"))
    handshake, zero_time = ser.send_handshake()
    if handshake:
        send_data = True

else:
    print(write_time("Running client script not detected"))

time.sleep(1)

# Send data if handshake received
if send_data:
    print(write_time("Sending ready signal"))
    ser.send_ready()

    print(write_time("Sending data"))
    # Bytes to send
    img = cv2.imread("test.jpg")
    print("Image size: {}".format(img.shape))
    data = np.reshape(img, -1)
    # data = range(0, 255)
    send = bytearray(data)
    print("Length of bytearray: {}".format(len(data)))
    ser.writeline("Data length:{}:{}:{}".format(img.shape[0], img.shape[1], img.shape[2]))

    ser.write_raw(send)

    print(write_time("Finished sending data"))

# Close serial port
ser.close()

print(write_time("Host script finished"))
