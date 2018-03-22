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
image_path = "/home/prospero/OBDA/simulation-test-bench/images/sample1/cam_imagery/time14.00s.jpg"
img = cv2.imread(image_path)
# print(img)
# print(type(img))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_dims = img.shape

# Send to client


# Receive altered image from client
progress = tqdm(total=img_dims[0]*img_dims[1]*img_dims[2])
total_bytes = 0
rcvd_acc = bytearray()
while total_bytes < img_dims[0]*img_dims[1]*img_dims[2]:
    num_bytes = ser.ser.in_waiting
    total_bytes += num_bytes
    # print("Num bytes: {}".format(num_bytes))
    # print("Total bytes: {}".format(total_bytes))
    rcvd = ser.ser.read(num_bytes)
    rcvd_acc.extend(rcvd)
    progress.update(num_bytes)
    # time.sleep(0.01)

data = np.array(list(rcvd_acc))
print("Number of bytes in data package: {}".format(len(data)))

data = np.reshape(data, img_dims)
# print(data)
# print(type(data))
if (data == img).all():
    print("Images are identical")

plt.imshow(data)
plt.show()

# Close serial port
print("Closing port")
ser.close()
