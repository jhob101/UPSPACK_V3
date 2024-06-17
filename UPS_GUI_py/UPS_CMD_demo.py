#!/usr/bin/python3

import re
import os
import sys
import time
from upspackv2 import *

# UPS initialization
test = UPS2("/dev/ttyAMA0")
load_time = time.time()

while True:
    try:
        time.sleep(2)
        version, vin, batcap, vout = test.decode_uart()
        cur_time = time.time()
        cur_time = cur_time - load_time

        print("Running:", int(cur_time), "s")

        batcap_int = int(batcap)

        if vin == "NG":
            print("Power NOT connected!")
        else:
            print("Power connected!")

        if batcap_int < 30:
            print("Battery Capacity:", batcap, "%")
            if batcap_int == 1:
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                stop_time = "\nHalt time :" + cur_time
                with open("log.txt", "a+") as f:
                    f.write(stop_time)
                os.system("sudo shutdown -t now")
                sys.exit()
        else:
            print("Battery Capacity:", batcap, "%")
        print("Output Voltage:", vout, "mV")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

