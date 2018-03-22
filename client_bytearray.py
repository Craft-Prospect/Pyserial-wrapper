#!/usr/bin/env python

"""client_bytearray.py: Client script for serial read/write"""

import time, cv2
import numpy as np
from serial_wrapper import Serial

# Create serial port object
ser = Serial("/dev/ttyPS0")
ser.flush()

# Check script is running
ser.writeline("Script running")

# Listen for handshake
zero_time = ser.listen_for_handshake()

# Wait for data signal
ser.get_ready()

# Receive data
# img_dims = (50, 200, 3)
# img_bytes = np.array(img_dims).prod()
# rcvd = ser.read_data(max_bytes=img_bytes)
# img = np.reshape(data, img_dims)

# Load image
image_path = "/home/xilinx/python/Pyserial-wrapper/test-small.jpg"
src = cv2.imread(image_path)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
mask = cv2.inRange(grey, 90, 255)
data = cv2.bitwise_and(img, img, mask=mask)

# Send ready command
ser.send_ready()
ser.get_ready()

time.sleep(0.5)

# Convert image to 1D list and send
data = list(np.reshape(data, -1))
send = bytearray(data)
ser.ser.write(send)

# Wait before ending so command line data doesn't get sent
time.sleep(5)

# Close serial port  
ser.close()
