#!/usr/bin/env python
#

import time
import string
import random
import argparse
import loremlogsum_http
import loremlogsum_stdout

def make_logs(timestamp, size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + ' '):
    return timestamp + ' ' + ''.join(random.choice(chars) for i in range(size))

def main():
    parser = argparse.ArgumentParser(description="Generate test log data")
    parser.add_argument("--time", metavar="seconds", required=False, default=5,
                        type=int, help="time to run in seconds (default 5)")
    parser.add_argument("--length", metavar="characters", default=120,
                        type=int, help="max number of characters per log line (default 120)")
    parser.add_argument("--rate", metavar="lines/sec attempted", default=8192,
                        type=int, help="max lines/sec to attempt writing (default 8192)")
    parser.add_argument("--module", metavar="writer", default='stdout',
                        type=str, help="set log sending module [stdout, http] (default stdout")
    parser.add_argument("--endpoint", metavar="http://logs.to/here", type=str,
                        help="where to send logs if module != stdout")
    parser.add_argument("--key", metavar="api_key", type=str,
                        help="api key, required for network modules")
    parser.add_argument("--burst", default=False, action='store_true',
                        help="randomize base rate around variance, with random bursts to\
                        10 * rate")
    parser.add_argument("--variance", metavar="0.2", default=0.2,
                        type=float, help="variance when using --burst, where base log rate\
                        will randomly vary between rate * (1-variance) and\
                        rate * (1+variance)")
    args = parser.parse_args()

    variance = args.variance

    if args.module == 'http':
        logger = loremlogsum_http.loremlogsum_http(args.key, args.endpoint)
    elif args.module == 'stdout':
        logger = loremlogsum_stdout.loremlogsum_stdout()

    start = int(time.time())
    now = int(time.time())
    length = args.length - len(str(now)) - 1

    while start + args.time > now:
        throttle = time.time()

        if args.burst:
            if random.choice(range(0, 100)) < 100 * variance:
                rate = args.rate * 10
            else:
                rate = random.choice(range(int(args.rate * (1 - variance)), int(args.rate * (1 + variance))))
        else:
            rate = args.rate

        for i in range(0,rate):
            logger.send(make_logs(str(now), length))
        if time.time() < throttle + 1:
            time.sleep(throttle + 1 - time.time())
        now = int(time.time())

if __name__ == "__main__":
    main()
