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

def client_comms():

    # Load image
    image_path = "test-small.jpg"
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_dims = img.shape
    img_bytes = np.array(img_dims).prod()

    # Send ready command
    ser.send_ready()

    time.sleep(0.5)

    # Send data
    data = list(np.reshape(img, -1))
    send = bytearray(data)
    ser.ser.write(send)

    time.sleep(1)

    # Wait for data signal
    ser.get_ready(verbal=True)

    ser.send_ready()

    # Receive data
    rcvd = ser.read_data(max_bytes=img_bytes, verbal=True)

    data = np.array(rcvd)
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

# Run client script
cmd = "python3.6 ~/python/Pyserial-wrapper/client_bytearray.py"
print("Sending command: {}".format(cmd))
ser.write_terminal_cmd(cmd)

time.sleep(0.5)

# Check script is running
check = ser.readline(5)

# Send handshake
if check != None and "running" in check:
    print("Running client script detected")
    handshake, zero_time = ser.send_handshake()

    if handshake:
        client_comms()

else:
    print("Running client script not detected")

# Close serial port
print("Closing port")
ser.close()
