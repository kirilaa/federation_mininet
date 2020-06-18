#!/usr/bin/python
import time
import os

if __name__ == '__main__':
    while True:
        stream = os.popen('ip a | grep 192.168.213').read()
        stream = stream.split('inet ',1)
        stream = stream[1].split('/',1)
        print(stream[0])
        print("Hey ho\n")
        timestamp = int(time.time())
        print("Time:", str("service"+str(timestamp)))
        time.sleep(2)
        