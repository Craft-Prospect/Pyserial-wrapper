#!/usr/bin/env python

"""host_bytearray.py: Host script for serial read/write"""

import time, cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from serial_wrapper import Serial

# Create serial object
ser = Serial("/dev/ttyUSB1")
ser.flush()

print("Check buffer: {}".format(ser.ser.in_waiting))

# Check it's open
if ser.is_open():
    print("Serial port is open")

# Run client script
cmd = "python3.6 ~/python/Pyserial-wrapper/client_bytearray.py"
print("Sending command: {}".format(cmd))
ser.write_terminal_cmd(cmd)

# Send handshake
handshake, zero_time = ser.send_handshake()

time.sleep(0.5)

# Load image
image_path = "test-small.jpg"
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_dims = img.shape
img_bytes = np.array(img_dims).prod()

# Send ready command
ser.send_ready()

# Wait for data signal
ser.get_ready(verbal=True)

# Receive data
rcvd_acc = ser.read_data(max_bytes=img_bytes)

data = np.array(rcvd_acc)
print("Number of bytes in data package: {}".format(len(data)))

data = np.reshape(data, img_dims)
# print(data)
# print(type(data))
if (data == img).all():
    print("Images are identical")

fig = plt.figure()
axs = fig.subplots(2, 1)
axs[0].imshow(img)
axs[1].imshow(data)
plt.show()

# Close serial port
print("Closing port")
ser.close()
