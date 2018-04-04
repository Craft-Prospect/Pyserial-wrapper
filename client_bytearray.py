#!/usr/bin/env python

"""client_bytearray.py: Client script for serial read/write"""

import time, cv2, os
import numpy as np
from serial_wrapper import Serial

time_start = time.time()

cur_dir = os.path.dirname(os.path.realpath(__file__))
log_file = cur_dir + "/client_log.txt"

# Pre-append time to log entry
def write_time(text):
    now = time.localtime(time.time())
    text = "{:02d}:{:02d}:{:02d} - {:s}".format(now[3], now[4], now[5], text)

    return text

# Script for saving data to log
def write2file(text, show_time=True):
    if text == "":
        show_time = False     
    with open(log_file, "a") as myfile:
        if type(text) is str:
            if show_time:
                text = write_time(text)
            myfile.write(text + "\n")
        elif type(text) is list:
            for line in text:
                if show_time:
                    line = write_time(line)
                myfile.write(line + "\n")

# Start log for file
now = time.localtime(time.time())
text = [
    "File: client_bytearray.py",
    time.asctime(now),
    ""
]
write2file(text, show_time=False)

# Create serial port object
ser = Serial("/dev/ttyPS0")
ser.flush()
write2file("Connected to serial port")

# Check script is running
ser.writeline("Script running")
write2file("Script running")

# Listen for handshake
zero_time = ser.listen_for_handshake()

# Wait for data signal
ready = ser.get_ready()
if ready:
    write2file("Ready signal received")
    write2file("")

    # Get data length
    rcvd = ser.readline(2)
    if "Data length" in rcvd:
        data_length = int(rcvd.split(":")[1])
        write2file("Incoming data length: {}".format(data_length))

    time.sleep(0.2)

    # Initialise
    t0 = time.time()
    t = 0
    total = 0
    data = bytearray()
    complete = False

    # Loop
    while t < 10 and complete == False:
        if total >= data_length:
            complete = True
        num_bytes = ser.in_waiting()
        total += num_bytes
        rcvd = ser.read_raw(num_bytes)
        data.extend(rcvd)
        savedata = "Bytes rec: {} - Total bytes: {}".format(num_bytes, total)
        if num_bytes > 0:
            write2file(savedata)
        time.sleep(0.01)
        t = time.time() - t0

    write2file("")

    data = np.array(list(data))

    write2file("check1")

    img = np.reshape(data, (50, 200, 3))

    write2file("check2")

    cv2.imwrite(cur_dir + "/output.jpg", img)

    write2file("check3")

else:
    write2file("Ready signal not received")

# Close serial port  
ser.close()

write2file("Client script finished")
write2file("", show_time=False)
