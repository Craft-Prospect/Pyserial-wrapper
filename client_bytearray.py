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

# Wait for data signal
# loop = True
# while loop:
#     time.sleep(0.5)
#     rcvd = ser.readline(timeout=0.02)
#     if rcvd != None and "ready" in rcvd:
#         loop = False

# # Receive data
# total_bytes = 0
# rcvd_acc = bytearray()
# while total_bytes < img_dims[0]*img_dims[1]*img_dims[2]:
#     num_bytes = ser.ser.in_waiting
#     total_bytes += num_bytes
#     rcvd = ser.ser.read(num_bytes)
#     rcvd_acc.extend(rcvd)
# img_list = np.array(list(rcvd_acc))
# img = np.reshape(data, (200, 50, 3))

# Load image
image_path = "/home/xilinx/python/cam_imagery/time14.00s.jpg"
src = cv2.imread(image_path)
print(src)
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
grey = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
mask = cv2.inRange(grey, 90, 255)
data = cv2.bitwise_and(img, img, mask=mask)

# Send ready command
ser.writeline("ready")

# Convert image to 1D list and send
data = list(np.reshape(data, -1))
send = bytearray(data)
ser.ser.write(send)

# Wait before ending so command line data doesn't get sent
time.sleep(5)

# Close serial port  
ser.close()
