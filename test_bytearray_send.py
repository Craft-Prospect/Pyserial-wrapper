#!/usr/bin/env python

"""test_bytearray_send.py: Send bytearray to PYNQ over serial"""

import serial, time, cv2
import numpy as np
from tqdm import tqdm

ser = serial.Serial("/dev/ttyUSB1", baudrate=115200, timeout=0)

print("Starting client")
ser.write(b"python3.6 ~/python/Pyserial-wrapper/test_bytearray_rec.py\n")

t0 = time.time()
while time.time() - t0 < 20:
    rcvd = ser.readline()
    # print(rcvd)
    if "Start" in rcvd.decode("ascii"):
        print("Client ready")
        break

time.sleep(2)

print("Writing data")

# Bytes to send
data = np.reshape(cv2.imread("test.jpg"), -1)
# data = range(0, 255)
send = bytearray(data)
print("Length of array: {}".format(len(data)))

ser.write(send)

print("Finished sending data")

time.sleep(2)

while time.time() - t0 < 100:
    rcvd = ser.readline()
    if rcvd != b"":
        print(rcvd.decode("ascii"))
        if "Done" in rcvd.decode("ascii"):
            print("Client finished")
            break

ser.close()
