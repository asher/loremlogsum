#!/usr/bin/env python
#
#

import time
import string
import random
import argparse

def make_logs(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + ' '):
    return ''.join(random.choice(chars) for i in range(size))

def main():
    parser = argparse.ArgumentParser(description="Generate test log data")
    parser.add_argument("--time", metavar="seconds", required=False, default=20,
                        type=int, help="time to run in seconds (default 20)")
    parser.add_argument("--length", metavar="characters", default=120,
                        type=int, help="max number of characters per log line (default 120")
    #parser.add_argument("--rate", metavar="lines/sec attempted", default=512,
    #                    type=int, help="lines/sec to attempt writing to stdout (default 120)")
    args = parser.parse_args()

   #time.time() == 1406915883.309331
    start = int(time.time())
    now = int(time.time())
    offset = len(str(now)) + 1

    make_logs(10)
    while start + args.time > now:
        for i in range(0,100):
            print "%f %s" % (now, make_logs(args.length - offset))
        now = int(time.time())

if __name__ == "__main__":
    main()
