#!/usr/bin/env python

"""client_bytearray.py: Client script for serial read/write"""

import time, cv2
import numpy as np
from serial_wrapper import Serial

# Settings
BUFFER_SIZE = 4096

# Create serial port object
ser = Serial("/dev/ttyPS0")
ser.flush()

# Listen for handshake
zero_time = ser.listen_for_handshake()

# Load image
image_path = "/home/xilinx/python/cam_imagery/time14.00s.jpg"
src = cv2.imread(image_path)
# print(src)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
grey = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
mask = cv2.inRange(grey, 90, 255)
data = cv2.bitwise_and(img, img, mask=mask)

# print(img)

# Convert image to 1D list and send
data = list(np.reshape(data, -1))
# print(data[:20])
# data = [0, 100, 200, 255]
send = bytearray(data)
# send = "This is a test string\n".encode("ascii")

ser.ser.write(send)

time.sleep(5)

# Close serial port  
ser.close()
