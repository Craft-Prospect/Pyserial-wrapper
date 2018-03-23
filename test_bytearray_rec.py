#!/usr/bin/env python3.6

"""test_bytearray_rec.py: Receive bytearray on PYNQ over serial"""

import serial, time, csv
# from pynq.overlays.base import BaseOverlay

# Load overlay
# overlay = BaseOverlay("base.bit")

# Turn on LEDs and set to red
# for ind in [4, 5]:
#     overlay.rgbleds[ind].on(4)

# Start serial port
ser = serial.Serial("/dev/ttyPS0", baudrate=115200, timeout=0)

# Set LEDs to green to indicate readiness
# for ind in [4, 5]:
#     overlay.rgbleds[ind].write(2)

time.sleep(0.2)

ser.write(b"Start\r\n")

# Read bytes
with open("/home/xilinx/python/Pyserial-wrapper/output.csv", "w") as csvfile:
    fieldnames = ["time", "num_bytes", "total_bytes"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Initialise
    t0 = time.time()
    t = 0
    total = 0
    data = bytearray()
    complete = False

    # Loop
    while t < 100 and complete == False:
        if total >= 480000:
            complete = True
        num_bytes = ser.in_waiting
        total += num_bytes
        rcvd = ser.read(num_bytes)
        data.extend(rcvd)
        savedata = {
            "time": round(t, 2),
            "num_bytes": num_bytes,
            "total_bytes": total
        }
        if num_bytes > 0:
            writer.writerow(savedata)
        # time.sleep(0.001)
        t = time.time() - t0

time.sleep(0.5)

send = "Time: {:.2f}s, bytes: {}\r\n".format(t-0.5, total)

ser.write(send.encode("ascii"))

time.sleep(0.5)

ser.write(b"Done\r\n")

time.sleep(1)

# Turn off LEDs
# for ind in [4, 5]:
#     overlay.rgbleds[ind].off()

# try:
#     ser.close()
# except NameError:
#     x = 0
